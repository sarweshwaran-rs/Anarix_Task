from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("Database URL not found, please set in")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_table_schema(session:Session, table_name: str) -> str:
    try:
        result = session.execute(text(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """))

        columns = []
        for row in result:
            columns.append(f"{row.column_name} {row.data_type.upper()}")

        schema = f"CREATE TABLE {table_name} (\n "+",\n ".join(columns) + "\n);"
        return schema
    except Exception as error:
        print(f"Error in fetching table schema for {table_name}: {error}")
        return ""
    

def get_all_table_schemas(session:Session) -> str:
    """Fetches schemas for all relevant tables"""
    table_names = [
        "product_level_ad_sales_and_metrics",
        "product_level_eligibility_table",
        "product_level_total_sales_and_metrics"
    ]

    all_schemas = []
    for table_name in table_names:
        schema = get_table_schema(session,table_name)
        if schema:
            all_schemas.append(schema)

    return "\n\n".join(all_schemas)