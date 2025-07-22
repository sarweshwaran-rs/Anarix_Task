import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        gemini_api = os.getenv("API_KEY")
        if not gemini_api:
            raise ValueError("API Key not found in environment Variable")
        genai.configure(api_key=gemini_api) # type: ignore

        self.model = genai.GenerativeModel('gemini-2.5-flash') # type: ignore

    def generate_sql(self, question:str, table: str) -> str:
        prompt = f""

        {table} # type: ignore

        "{question}"

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as error:
            print(f"Error generating the SQL Query with LLM: {error}")
            return "Error: Could not generate SQL query"
        