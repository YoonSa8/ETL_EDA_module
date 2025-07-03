
import pandas as pd

def generate(df: pd.DataFrame, method: str = "profile", output_path: str = "eda_report.html"):
    print(f"[INFO] Generating EDA report using: {method}")
    try:
        if method == "profile":
            from ydata_profiling import ProfileReport
            profile = ProfileReport(df, title="EDA Report", explorative=True)
            profile.to_file(output_path)

        elif method == "sweetviz":
            import sweetviz as sv
            report = sv.analyze(df)
            report.show_html(filepath=output_path)

        else:
            raise ValueError(f"Unsupported EDA method: {method}")

        print(f"[INFO] EDA report saved to: {output_path}")

    except Exception as e:
        print(f"[ERROR] Failed to generate EDA report: {e}")
        raise
