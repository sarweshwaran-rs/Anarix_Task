import pandas as pd
from sqlalchemy import create_engine

def load_data(db_url, excel_path):
    engine = create_engine(db_url)
    df = pd.read_excel(excel_path, sheet_name=None)

    for sheet, data in df.items():
        data.to_sql(sheet.lower(), con=engine, if_exists='replace', index=False)
    print("Data loaded to SQL Successfully")