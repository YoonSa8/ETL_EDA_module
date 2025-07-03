# transform/clean_transform.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from pandas.api.types import is_string_dtype, is_numeric_dtype

def process(df: pd.DataFrame, config: dict = {}) -> pd.DataFrame:
    print(f"[INFO] Starting transformation on data with shape {df.shape}")
    df = df.copy()

    # 1. Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # 2. Rename columns if mapping is provided
    col_map = config.get("column_rename_map", {})
    if col_map:
        df.rename(columns=col_map, inplace=True)
        print(f"[INFO] Renamed columns: {col_map}")

    # 3. Drop duplicates
    if config.get("drop_duplicates", True):
        before = df.shape[0]
        df.drop_duplicates(inplace=True)
        after = df.shape[0]
        print(f"[INFO] Dropped {before - after} duplicate rows")

    # 4. Handle missing values (median for numeric, mode for object)
    for col in df.columns:
        if df[col].isnull().any():
            if is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
            elif is_string_dtype(df[col]):
                df[col].fillna(df[col].mode()[0], inplace=True)

    # 5. Infer types (e.g., convert strings to datetime if possible)
    for col in df.columns:
        if is_string_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                continue  # leave as string if conversion fails

    # 6. Encode categorical variables
    encoding_type = config.get("encoding", None)  # "label" or "onehot"
    if encoding_type:
        cat_cols = df.select_dtypes(include='object').columns
        if encoding_type == "label":
            for col in cat_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
            print(f"[INFO] Label encoded columns: {list(cat_cols)}")
        elif encoding_type == "onehot":
            df = pd.get_dummies(df, columns=cat_cols)
            print(f"[INFO] One-hot encoded columns: {list(cat_cols)}")

    # 7. Normalize or Standardize numerical data
    scaling = config.get("scaling", None)  # "standard" or "minmax"
    if scaling:
        numeric_cols = df.select_dtypes(include='number').columns
        if scaling == "standard":
            scaler = StandardScaler()
        elif scaling == "minmax":
            scaler = MinMaxScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        print(f"[INFO] Applied {scaling} scaling to: {list(numeric_cols)}")

    print(f"[INFO] Final shape after transform: {df.shape}")
    return df
