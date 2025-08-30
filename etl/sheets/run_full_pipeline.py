import os
import snowflake.connector
from dotenv import load_dotenv
import subprocess

# -------------------------------------------------------------------
# 1. Load environment variables
# -------------------------------------------------------------------
env_path = os.path.join(os.path.dirname(__file__), "../../config/.env")
print("Looking for env at:", env_path)
load_dotenv(dotenv_path=env_path)

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")

SQL_FILES = [
    "db/stg_load.sql",
    "db/dim_load.sql",
    "db/fact_load.sql"
]

# -------------------------------------------------------------------
# 2. Run SQL file in Snowflake (split by ;)
# -------------------------------------------------------------------
def run_sql_file(path):
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE
    )
    cur = conn.cursor()
    print(f"▶ Running SQL file: {path}")

    with open(path, "r") as f:
        sql_content = f.read()

    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

    for stmt in statements:
        print(f"   → Executing: {stmt[:60]}...")  # preview first 60 chars
        cur.execute(stmt)

    cur.close()
    conn.close()

# -------------------------------------------------------------------
# 3. Main
# -------------------------------------------------------------------
def main():
    print("🚀 Running FULL pipeline (Initial Load + STG + DIM + FACT)")
    
    # Step 1: Full load from Google Sheets → RAW
    subprocess.run(["py", "-3.13", "etl/sheets/load_initial.py"], check=True)

    # Step 2: Run STG, DIM, FACT SQL scripts
    for sql_file in SQL_FILES:
        run_sql_file(sql_file)

    print("🎉 Full pipeline completed successfully!")

if __name__ == "__main__":
    main()