from config import CONFIG
from ETL_EDA_module.extract.from_csv import from_csv, from_sql, from_api
from transform import clean_transform
from load import to_storage
from EDA import eda_report
import pandas as pd

def extract_data():
    source = CONFIG['source']
    if source == "csv":
        return from_csv.load_csv(CONFIG['csv_path'])
    elif source == "sql":
        return from_sql.load_sql(CONFIG['sql']['connection_string'], CONFIG['sql']['query'])
    elif source == "api":
        api_conf = CONFIG['api']
        return from_api.load_api(
            url=api_conf['url'],
            api_key=api_conf['api_key'],
            params=api_conf.get('params', {}),
            auth_header=api_conf.get('auth_header', 'Authorization'))    
    else:
        raise ValueError(f"Unsupported data source: {source}")
    
def load_data(df: pd.DataFrame):
    load_config = CONFIG.get("load", {})
    load_type = load_config.get("type")

    if load_type == "csv":
        to_storage.save_to_csv(df, load_config["csv_path"])
    elif load_type == "sql":
        sql_conf = load_config["sql"]
        to_storage.save_to_sql(
            df,
            connection_string=sql_conf["connection_string"],
            table_name=sql_conf["table_name"],
            if_exists=sql_conf.get("if_exists", "replace")
        )
    else:
        raise ValueError(f"[ERROR] Unknown load type: {load_type}")

def run_pipeline():
    df = extract_data()
    df_clean = clean_transform.process(df_raw, config=CONFIG.get("transform", {}))
    load_data(df_clean)
    eda_config = CONFIG.get("eda", {})
    if eda_config.get("enabled", False):
        eda_report.generate(
            df_clean,
            method=eda_config.get("method", "profile"),
            output_path=eda_config.get("output_path", "eda_report.html")
        )

if __name__ == "__main__":
    run_pipeline()
