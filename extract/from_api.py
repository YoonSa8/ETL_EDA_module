
import pandas as pd
import requests

def load_api(url: str, api_key: str, params: dict = {}, auth_header: str = "Authorization") -> pd.DataFrame:
    try:
        headers = {auth_header: f"Bearer {api_key}"}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Try handling list or nested dict formats
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            key = next((k for k in data if isinstance(data[k], list)), None)
            df = pd.DataFrame(data[key]) if key else pd.json_normalize(data)
        else:
            raise ValueError("Unsupported API response format")

        print(f"[INFO] Loaded API data from {url} with shape {df.shape}")
        return df

    except Exception as e:
        print(f"[ERROR] API extraction failed: {e}")
        raise
