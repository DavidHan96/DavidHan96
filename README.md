# 📊 David’s Analytics Dashboards Portfolio

End-to-end data project demonstrating my ability to:
- Ingest data → Model with a **star schema** → Visualize and operate dashboards.
- Land pipelines in **Snowflake** and power interactive **Looker Studio** dashboards.

---

## 🎯 Why I Built This
Practical, production-minded skills across the full stack:
- Data ingestion & transformation  
- Dimensional modeling (STG → FACT → VIEWs)  
- Dashboarding with filters, rollups, and smart rankings  
- All **automated and version-controlled**  

---

## 🚀 Live Dashboards

### 🔹 Job Applications Analytics
_End-to-end funnel tracking across role/industry distribution._

[![Job Applications Analytics](dashboards/job_applications/Job_Applications_Analytics.png)](https://lookerstudio.google.com/reporting/05a43d81-625f-4196-8616-76beb82abf3a "Open in Looker Studio")

Features:
- Smart Rankings (companies, counts, averages)  
- Application funnel (applied → interviewed → offer)  
- Weekly & cumulative trends  
- Role/Industry distributions  

---

### 🔹 Study Log Analytics
_Daily hours & problems solved, with moving averages and category insights._

[![Study Log Analytics](dashboards/study_log/Study_Log_Analytics.png)](https://lookerstudio.google.com/reporting/edeb330e-5a46-4eda-b1e1-1941c14eb872 "Open in Looker Studio")

Features:
- Daily study hours + 7-day moving averages  
- Category share donut (Google color palette)  
- Smart Rankings (Hours / Problems / Difficulty)  
- Session-level details  

---

## 🧱 Architecture

**Pipeline:**  
`Google Sheets → ETL (Python) → Snowflake (STG/FACT/VIEWs) → Looker Studio`

```text
Raw study & jobs  -->  etl/sheets/load_initial.py   # bootstrap load
                    etl/sheets/incremental_load.py # periodic updates

STG:  db/stg_load.sql          # typed staging
FACT: db/fact_load.sql         # session/application facts
VIEW: db/VW_STUDY_LOG.sql      # reporting-friendly columns
📥 Source Data (Google Sheets)
<p align="center"> <img src="dashboards/job_applications/application_google_sheet.png" alt="Job Applications — Google Sheet preview" width="48%" /> <img src="dashboards/study_log/study_log_google_sheet.png" alt="Study Log — Google Sheet preview" width="48%" /> </p>
✨ Features
Common

Automated ingestion from Google Sheets

Snowflake warehouse (SQL transformations, window functions, rollups)

Looker Studio dashboards with global filters

Reproducible pipelines + versioned SQL/ETL

Job Applications Analytics

Smart ranking, Funnel conversion

Weekly & cumulative trends

Role/Industry splits

Study Log Analytics

7-day moving averages for hours/problems

Category share with % labels

Parameterized Smart Rankings

Detailed session drilldowns

🛠️ Tech Stack
Warehouse: Snowflake (window functions, analytic views)

ETL: Python (pandas loaders)

Modeling: SQL (db/*.sql)

Visualization: Looker Studio (filters, parameters, calculated fields)

Version Control: GitHub

📂 Repository Structure
text
Copy code
.
├─ dashboards/
│  ├─ job_applications/
│  │  ├─ Job_Applications_Analytics.png
│  │  ├─ application_google_sheet.png
│  │  └─ README.md
│  ├─ study_log/
│  │  ├─ Study_Log_Analytics.png
│  │  ├─ study_log_google_sheet.png
│  │  └─ README.md
│  └─ README.md                # folder index of dashboards
├─ db/
│  ├─ stg_load.sql             # staging transforms
│  ├─ fact_load.sql            # fact transforms
│  └─ VW_STUDY_LOG.sql         # reporting view
├─ etl/
│  └─ sheets/
│     ├─ load_initial.py       # one-time bootstrap from Sheets
│     └─ incremental_load.py   # periodic updates
└─ data/                        # placeholders / examples (gitkept)
⚙️ Reproduce Locally (Quick Start)
Snowflake

bash
Copy code
export SNOWFLAKE_ACCOUNT=...
export SNOWFLAKE_USER=...
export SNOWFLAKE_PASSWORD=...
export SNOWFLAKE_WAREHOUSE=...
export SNOWFLAKE_ROLE=...
export SNOWFLAKE_DATABASE=JOBDASH
export SNOWFLAKE_SCHEMA=ANALYTICS
Google Sheets
Provide the Sheet IDs/creds in etl/sheets/*.py, then run:

bash
Copy code
python etl/sheets/load_initial.py       # first load
python etl/sheets/incremental_load.py   # subsequent runs
SQL modeling order

sql
Copy code
-- staging
run db/stg_load.sql;

-- facts
run db/fact_load.sql;

-- views
run db/VW_STUDY_LOG.sql;
Then connect Looker Studio → Snowflake Views → Publish 🚀

🧭 Roadmap
🔹 MCP integration (Model Context Protocol): Natural Language → SQL copilots

🔹 dbt migration (tests, docs, environments)

🔹 CI/CD checks (SQL lint, unit tests, data freshness SLAs)

🔹 Operational dashboards (SLA monitors, error surfacing)

👤 My Role & Contributions
Designed & implemented full pipeline (Sheets → Snowflake → Looker Studio)

Authored staging/fact SQL, reporting views, and dashboards

Built ETL scripts for initial & incremental loads

UX consistency (Google palette, filters, Smart Rankings)

Wrote docs and automated exports