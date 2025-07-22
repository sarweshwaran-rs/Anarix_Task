import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def load_data_from_csvs(db_url, csv_directory):
    
    engine = create_engine(db_url)
    
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in the directory: {csv_directory}")
        return

    print(f"Found {len(csv_files)} CSV files in '{csv_directory}'. Starting data loading...")

    for csv_file in csv_files:
        file_path = os.path.join(csv_directory, csv_file)
        
        
        base_name = os.path.splitext(csv_file)[0]
        
        if ' - ' in base_name:
            parts = base_name.split(' - ')
            clean_name_part = parts[-1].replace(' (mapped).xlsx', '').strip()
        else:
            clean_name_part = base_name.strip()
            
        table_name = clean_name_part.lower().replace(' ', '_').replace('-', '_').replace('.', '_')
        
        table_name = '_'.join(filter(None, table_name.split('_'))) 
        table_name = table_name.strip('_') 

        try:
            df = pd.read_csv(file_path)
            
            df.columns = [col.lower() for col in df.columns]

            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"Data from '{csv_file}' loaded to SQL table '{table_name}' successfully.")
        except Exception as e:
            print(f"Error loading data from '{csv_file}' to SQL table '{table_name}': {e}")
            
    print("\nAll specified CSV data loading process completed.")

if __name__ == "__main__":
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL not found in environment variables. Please set it in your .env file.")
    
    csv_data_directory = os.path.join(os.path.dirname(__file__), 'data') 
    
    load_data_from_csvs(db_url, csv_data_directory)