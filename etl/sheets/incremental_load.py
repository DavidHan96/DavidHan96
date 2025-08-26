# etl/sheets/incremental_load.py
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
    """Normalize types for incremental upsert. Handles serial dates + ISO text."""
    df = df.copy()
    df.columns = [c.upper() for c in df.columns]

    # --- handle BOTH ISO/text dates and Google Sheets serial numbers ---
    def to_date(col: str):
        if col not in df.columns: return
        s = df[col]
        s_num = pd.to_numeric(s, errors="coerce")
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
        # Snowflake TIMESTAMP_NTZ(3) friendly string
        df[col] = ts.dt.strftime("%Y-%m-%d %H:%M:%S.%f").str[:-3]

    to_date("DATE_APPLIED")
    to_date("SESSION_DATE")
    to_ts("CREATED_AT")
    to_ts("LAST_MODIFIED")

    for c in ["APP_ID", "STUDY_ID", "COMPENSATION", "PROBLEMS_SOLVED", "HOURS"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # empty strings -> None
    df = df.where(df.notna() & (df.astype(str).ne("")), None)
    return df

def merge_dataframe(conn, df: pd.DataFrame, target: str, pk: str):
    """Upload to a temp table and MERGE by PK.
       Update when target.last_modified is NULL OR source >= target.
       Insert when not matched.
    """
    if df.empty:
        print(f"ℹ️ No rows to process for {target}")
        return

    cur = conn.cursor()
    temp = f"{target}_TEMP"
    cur.execute(f"CREATE OR REPLACE TEMPORARY TABLE {temp} AS SELECT * FROM {target} WHERE 1=0")
    write_pandas(conn, df.reset_index(drop=True), temp)

    set_clause = ", ".join([f"t.{c}=s.{c}" for c in df.columns if c.upper() != pk.upper()])
    cols = ", ".join(df.columns)
    vals = ", ".join([f"s.{c}" for c in df.columns])

    # NOTE: NVL/COALESCE guard so NULL or equal timestamps still update
    merge_sql = f"""
        MERGE INTO {target} t
        USING {temp} s
        ON t.{pk} = s.{pk}
        WHEN MATCHED AND NVL(t.LAST_MODIFIED, TO_TIMESTAMP_NTZ('1900-01-01 00:00:00.000'))
                        <= NVL(s.LAST_MODIFIED, TO_TIMESTAMP_NTZ('1900-01-01 00:00:00.000'))
        THEN UPDATE SET {set_clause}
        WHEN NOT MATCHED THEN
          INSERT ({cols}) VALUES ({vals});
    """
    cur.execute(merge_sql)
    print(f"✅ Upsert done for {target}")

def main():
    print(">>> Incremental load started")
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
        # Applications → MERGE (update if last_modified is newer OR equal, or target is NULL)
        rows_app = read_unformatted(client, GOOGLE_SHEET_ID, "applications")
        if rows_app:
            df_app = normalize(pd.DataFrame(rows_app))
            df_app["APP_ID"] = pd.to_numeric(df_app.get("APP_ID"), errors="coerce")
            df_app = df_app[df_app["APP_ID"].notna()]
            merge_dataframe(conn, df_app, "JOB_APPLICATIONS_RAW", "APP_ID")
        else:
            print("⚠️ No data in sheet applications")

        # Study logs → append-only (insert if new STUDY_ID)
        rows_study = read_unformatted(client, GOOGLE_SHEET_ID, "study_logs")
        if rows_study:
            df_study = normalize(pd.DataFrame(rows_study))
            df_study["STUDY_ID"] = pd.to_numeric(df_study.get("STUDY_ID"), errors="coerce")
            df_study = df_study[df_study["STUDY_ID"].notna()]

            cur = conn.cursor()
            temp = "STUDY_LOG_RAW_TEMP"
            cur.execute(f"CREATE OR REPLACE TEMPORARY TABLE {temp} AS SELECT * FROM STUDY_LOG_RAW WHERE 1=0")
            write_pandas(conn, df_study.reset_index(drop=True), temp)

            merge_sql = f"""
                MERGE INTO STUDY_LOG_RAW t
                USING {temp} s
                ON t.STUDY_ID = s.STUDY_ID
                WHEN NOT MATCHED THEN
                  INSERT ({", ".join(df_study.columns)})
                  VALUES ({", ".join([f"s.{c}" for c in df_study.columns])});
            """
            cur.execute(merge_sql)
            print("✅ Insert-if-new done for STUDY_LOG_RAW")
        else:
            print("⚠️ No data in sheet study_logs")

        print("🎉 Incremental load finished successfully!")
    finally:
        conn.close()
        print("🔌 Snowflake connection closed.")

if __name__ == "__main__":
    main()
