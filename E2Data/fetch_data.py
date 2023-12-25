import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def fetch_data():
    try:
        # Create an SQLAlchemy engine
        engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

        # Query to fetch data from the E2Data table
        query = "SELECT * FROM E2Data"

        # Fetch data into a pandas DataFrame
        df = pd.read_sql(query, engine)

        # Close the SQLAlchemy engine
        engine.dispose()

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    data = fetch_data()

    if data is not None:
        print(data.head())
