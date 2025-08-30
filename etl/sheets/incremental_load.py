# etl/sheets/load_initial.py
import os
import sys
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# --- env ---
env_path = os.path.join(os.path.dirname(__file__), "../../config/.env")
load_dotenv(dotenv_path=env_path)

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Sheet -> RAW table mapping
SHEETS = {
    "applications": "JOB_APPLICATIONS_RAW",
    "study_logs":   "STUDY_LOG_RAW",
}

def get_gs_client():
    """Authorize and return a gspread client."""
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scopes)
    return gspread.authorize(creds)

def read_unformatted(client, sheet_id, worksheet):
    """Read raw/unformatted values. get_all_records supports value_render_option only."""
    ws = client.open_by_key(sheet_id).worksheet(worksheet)
    return ws.get_all_records(
        value_render_option="UNFORMATTED_VALUE",
        head=1,
    )

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize types for Snowflake RAW. Handles text dates and Google Sheets serial dates."""
    df = df.copy()
    df.columns = [c.upper() for c in df.columns]

    # helpers that handle BOTH ISO/text dates and Google Sheets serial numbers
    def to_date(col: str):
        if col not in df.columns: return
        s = df[col]
        s_num = pd.to_numeric(s, errors="coerce")  # serial days
        dt_num = pd.to_datetime(s_num, errors="coerce", unit="D", origin="1899-12-30")
        s_txt = s.where(s_num.isna())
        dt_txt = pd.to_datetime(s_txt, errors="coerce", utc=True)
        dt = dt_txt.fillna(dt_num)
        df[col] = dt.dt.date

    def to_ts(col: str):
        if col not in df.columns: return
        s = df[col]
        s_num = pd.to_numeric(s, errors="coerce")
        ts_num = pd.to_datetime(s_num, errors="coerce", unit="D", origin="1899-12-30")
        s_txt = s.where(s_num.isna())
        ts_txt = pd.to_datetime(s_txt, errors="coerce", utc=True)
        ts = ts_txt.fillna(ts_num)
        df[col] = ts.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]  # millisecond precision

    # apply conversions
    to_date("DATE_APPLIED")
    to_date("SESSION_DATE")
    to_ts("CREATED_AT")
    to_ts("LAST_MODIFIED")

    # numerics
    for c in ["APP_ID", "STUDY_ID", "COMPENSATION", "PROBLEMS_SOLVED", "HOURS"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # optional boolean mapping
    if "IS_DELETED" in df.columns:
        df["IS_DELETED"] = df["IS_DELETED"].map(
            lambda x: True if str(x).lower() in ("true","yes","1") else
                      False if str(x).lower() in ("false","no","0") else None
        )

    # empty strings -> None
    df = df.where(df.notna() & (df.astype(str).ne("")), None)
    return df

def main():
    print(">>> Initial load started")
    print("gspread:", gspread.__version__, "| python:", sys.version.split()[0])

    client = get_gs_client()
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    print("✅ Connected to Snowflake")

    try:
        for sheet_name, table_name in SHEETS.items():
            rows = read_unformatted(client, GOOGLE_SHEET_ID, sheet_name)
            if not rows:
                print(f"⚠️ No data in sheet {sheet_name}")
                continue

            df = normalize(pd.DataFrame(rows))
            print(f"\n📊 Preview {sheet_name}:")
            print(df.head(2))

            cur = conn.cursor()
            cur.execute(f"TRUNCATE TABLE {table_name}")
            write_pandas(conn, df, table_name.upper())
            print(f"✅ Loaded {len(df)} rows into {table_name}")

        print("🎉 All data loaded successfully!")
    finally:
        conn.close()
        print("🔌 Snowflake connection closed.")

if __name__ == "__main__":
    main()