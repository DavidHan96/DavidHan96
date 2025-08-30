import os
import sys
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

def get_gs_client():
    creds = Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=[
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    return gspread.authorize(creds)

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.upper() for c in df.columns]

    for col in df.columns:
        if "DATE" in col.upper():
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
        if "CREATED_AT" in col.upper() or "LAST_MODIFIED" in col.upper():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

SHEETS = {
    "applications": "JOB_APPLICATIONS_RAW",
    "study_logs": "STUDY_LOG_RAW",
}

def main():
    print(">>> Initial load started")
    client = get_gs_client()
    conn = get_snowflake_conn()
    print("✅ Connected to Snowflake")

    try:
        for sheet_name, table_name in SHEETS.items():
            rows = client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).worksheet(sheet_name).get_all_records()
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
