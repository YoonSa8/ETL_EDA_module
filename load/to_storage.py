
import pandas as pd
from sqlalchemy import create_engine

def save_to_csv(df: pd.DataFrame, path: str):
    try:
        df.to_csv(path, index=False)
        print(f"[INFO] Data saved to CSV at: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to save CSV: {e}")
        raise

def save_to_sql(df: pd.DataFrame, connection_string: str, table_name: str, if_exists: str = "replace"):
    try:
        engine = create_engine(connection_string)
        df.to_sql(table_name, con=engine, index=False, if_exists=if_exists)
        print(f"[INFO] Data saved to SQL table '{table_name}'")
    except Exception as e:
        print(f"[ERROR] Failed to save to SQL: {e}")
        raise
