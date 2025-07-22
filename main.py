from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from llm.agent import AIAgent
from db.connection import get_db, get_all_table_schemas
from db.queries import execute_sql

import uvicorn
import os

app = FastAPI(
    title="E-Commerce AI Agent",
    description="An AI Agent Which answers the users Questions",
    version="0.1.0"
    )

try:
    ai_agent = AIAgent()
except ValueError as error:
    print(f"Failed to initialize the AI Agent")
    exit(1)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    ori_question: str
    sql_query_gen: str
    answer_data: List[Dict[str, Any]]
    message: str = "Query executed Successfully"

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    
    table_schemas = get_all_table_schemas(db)

    if not table_schemas:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve database schemas. Please ensure tables are populated"
        )
    
    generated_query = ai_agent.generate_sql(question=request.question, table=table_schemas)

    if "Error: Could not generate SQL query" in generated_query:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI Agent failed to generate the query, Please try rephrasing"
        )
    
    print(f"Executing SQL: {generated_query}")
    query_result = execute_sql(db, generated_query)

    if any("error" in res for res in query_result):
        error_detail = query_result[0].get("error", "Unknown database error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail=f"Database query failed:{error_detail}. Generated SQL: {generated_query}" 
                        )
    return AnswerResponse(
        ori_question=request.question,
        sql_query_gen=generated_query,
        answer_data=query_result,
        message="Query executed successfully"
    )

@app.get("/")
async def read_root():
    return {"message": "AI E-Commerce Data Agent is running. Use /ask endpoint for questions"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)