#importing the necessary libraries
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        #loading the Gemini API key from the environment
        gemini_api = os.getenv("API_KEY")
        if not gemini_api:
            raise ValueError("API Key not found in environment Variable")
        genai.configure(api_key=gemini_api) # type: ignore
        self.model = genai.GenerativeModel('gemini-2.5-flash') # type: ignore

    #Defining the function to create the SQL from the question
    def generate_sql(self, question:str, table: str) -> str:
        prompt = f"""
        You have access to the following database tables:
        {table} 
        Generate me the postgreSQL query for the following question:
        "{question}"
        And ensure it is the valid for PostgreSQL and only return the SQL Query, no additional information.
        """
        try:
            response = self.model.generate_content(prompt)
            query = response.text.strip()
            query = query.replace('```sql','').replace('```','').strip()
            return query
        except Exception as error:
            print(f"Error generating the SQL Query with LLM: {error}")
            return "Error: Could not generate SQL query"
        