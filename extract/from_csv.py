
import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        print(f"[INFO] Loaded CSV from {path} with shape {df.shape}")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        raise
