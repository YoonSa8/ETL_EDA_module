CONFIG = {
    "source": "csv",  
    "csv_path": "data/sample.csv",
    "sql": {
        "connection_string": "D:\software_program\sqlite_dbs\localhost",
        "query": "SELECT * FROM tabel1"
    },
    "api": {
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "api_key" :"0835ff2d40b8180cfa94e1c9ea38a9dc",
        "headers": {},
        "params": {
            "limit": 100,
            "sort": "desc"
        }
    },
    "transform": {
            "column_rename_map": {
                "First Name": "first_name",
                "Last Name": "last_name"
            },
            "drop_duplicates": True,
            "encoding": "label",      # "label", "onehot", or None
            "scaling": "standard"     # "standard", "minmax", or None
        },

    "load": {
        "type": "csv",  # or "sql"
        "csv_path": "data/cleaned_output.csv",
        "sql": {
            "connection_string": "sqlite:///data/output.db",
            "table_name": "cleaned_data",
            "if_exists": "replace"  # or "append"
        }
    },
    "eda": {
        "enabled": True,
        "method": "profile",   # "profile" or "sweetviz"
        "output_path": "eda_report.html"
    }
}
