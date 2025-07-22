import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        gemini_api = os.getenv("API_KEY")

        if not gemini_api:
            raise ValueError(f"API Key not found in Environment")
        genai.configure(api_key=gemini_api)

        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_sql(self, question: str, table: str) -> str:

        prompt = f""

        {table}

        "{question}"

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error in Generating the SQL query: {e}")
            return "Error: Could not generate the SQL query"
        
         