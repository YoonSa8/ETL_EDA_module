
import pandas as pd
from sqlalchemy import create_engine

def load_sql(connection_string: str, query: str) -> pd.DataFrame:
    try:
        engine = create_engine(connection_string)
        df = pd.read_sql_query(query, con=engine)
        print(f"[INFO] Loaded SQL data with shape {df.shape}")
        return df
    except Exception as e:
        print(f"[ERROR] SQL extraction failed: {e}")
        raise
