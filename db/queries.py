from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any


def execute_sql(db: Session, sql_query: str) -> List[Dict[str, Any]]:

    try:
        result = db.execute(text(sql_query))

        rows = result.fetchall()
        if rows:
            columns = result.keys()
            rows_as_dicts = [dict(zip(columns, row)) for row in rows]
            return rows_as_dicts
        else:
            return [{"message": "Query executed successfully, no data returned", "rows_affected": len(rows)}]
    except Exception as error:
        print(f"Error executing SQL Query: {error}")
        print(f"Problematic Query: {sql_query}")
        return [{"error":str(error), "query":sql_query}]