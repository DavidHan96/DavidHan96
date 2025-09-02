David’s Analytics Dashboards Portfolio

End-to-end data project demonstrating my ability to ingest data → model with a star schema → visualize and operate dashboards.
Pipelines land in Snowflake and power interactive Looker Studio dashboards.

Why I built this
To show practical, production-minded skills across the full stack: data ingestion, transformation, dimensional modeling, and dashboarding—all automated and version-controlled.

🚀 Live Dashboards

Job Applications Analytics → Open README

(smart rankings, funnel, weekly trend, role/industry distribution)

Study Log Analytics → Open in Looker Studio
 · Project README

(daily hours & problems solved with 7-day moving average, category share, smart rankings, session details)

🧱 Architecture (Sheets → Snowflake → Looker Studio)
Google Sheets          ETL (Python)                 Snowflake                     Looker Studio
------------------     -------------------------    ---------------------------    ----------------------------
Raw study & jobs  -->  etl/sheets/load_initial.py   RAW / STG schemas             Interactive dashboards
(appendable logs)      etl/sheets/incremental_load.py
                       db/stg_load.sql
                       db/fact_load.sql             FACT tables
                                                   + Views (VW_* for reporting)


Modeling approach

STG: cleaned, typed staging tables

FACT: session/application grain facts with consistent keys

VIEWs: reporting-friendly columns (derived metrics, mappings, rolling averages)

✨ Features
Common

Automated ingestion from Google Sheets

Snowflake as the warehouse (SQL transformations, window functions, rollups)

Looker Studio dashboards with global date/category filters

Reproducible pipeline + versioned SQL/ETL in Git

Job Applications Analytics

Smart ranking (companies, counts, averages)

Funnel (applied → interviewed → offer)

Weekly & cumulative trends

Role/industry distributions

Study Log Analytics

Daily study hours & problems solved + 7-day moving averages

Category share donut (Google color palette)

Smart Rankings with parameterized sorting (Hours / Problems / Difficulty)

Session-level details table (date, category, topic, provider, difficulty)

🛠️ Tech Stack

Warehouse: Snowflake (WINDOW functions, analytic views)

ETL: Python (pandas) + simple loaders (etl/sheets/*.py)

Modeling: SQL in db/*.sql (STG, FACT, and reporting VIEWs)

Viz: Looker Studio (filters, parameters, calculated fields)

VCS: GitHub

📁 Repository Structure
.
├─ dashboards/
│  ├─ job_applications/
│  │  ├─ Job_Applications_Analytics.pdf
│  │  └─ README.md
│  ├─ study_log/
│  │  ├─ Study_Log_Analytics.pdf
│  │  └─ README.md
│  └─ README.md                # folder index of dashboards
├─ db/
│  ├─ stg_load.sql             # staging transforms
│  ├─ fact_load.sql            # fact transforms
│  └─ VW_STUDY_LOG.sql         # reporting view (rolling avgs, category share, etc.)
├─ etl/
│  └─ sheets/
│     ├─ load_initial.py       # one-time bootstrap from Sheets
│     └─ incremental_load.py   # small periodic updates
└─ data/                        # placeholders / examples (gitkept)

⚙️ Reproduce Locally (quick start)

Snowflake env vars (or use a .env):

export SNOWFLAKE_ACCOUNT=...
export SNOWFLAKE_USER=...
export SNOWFLAKE_PASSWORD=...
export SNOWFLAKE_WAREHOUSE=...
export SNOWFLAKE_ROLE=...
export SNOWFLAKE_DATABASE=JOBDASH
export SNOWFLAKE_SCHEMA=ANALYTICS


Google Sheets: provide the Sheet IDs/creds in the ETL scripts (see etl/sheets/*.py), then run:

python etl/sheets/load_initial.py       # first load
python etl/sheets/incremental_load.py   # subsequent runs


SQL modeling (order):

-- staging
-- run contents of db/stg_load.sql

-- facts
-- run contents of db/fact_load.sql

-- views (example)
-- run contents of db/VW_STUDY_LOG.sql


Connect Looker Studio to the Snowflake views and publish.

🔍 Example: Study Log reporting view

db/VW_STUDY_LOG.sql produces the fields used by the dashboard, including:

ROLLING_7D_AVG_HOURS, ROLLING_7D_AVG_PROBLEMS

CATEGORY_SHARE (nice label like “Data Engineering (54.5%)”)

DIFFICULTY_SCORE mapping, IS_PROJECT, PROJECT_HOURS, etc.

🧭 Roadmap

MCP integration (Model Context Protocol)

Connect Snowflake to GenAI copilots (GPT, Claude, Gemini) via MCP

Secure, auditable access patterns for data-aware assistants

Natural Language → SQL

NL prompts into parameterized, reviewable SQL against the warehouse

Guardrails + query templates; explain plans + cost hints in UI

dbt migration

Port stg_* / fact_* SQL to dbt with tests, docs, and environments

CI/CD

Lightweight checks (SQL lint, unit tests for Python loaders)

Operational dashboards

Data freshness KPIs, SLA monitors, load error surfacing

👤 My Role & Contributions

Designed & implemented the end-to-end pipeline (Sheets → Snowflake → Looker Studio)

Authored staging/fact SQL, reporting views, and parameterized dashboard logic

Built ETL scripts for initial & incremental loads

Set up color/UX consistency (Google palette), filters, and smart rankings

Wrote documentation and automated exports (PDFs in dashboards/*)

📫 Contact

Questions or collaboration ideas? Open an issue, or reach me on GitHub @DavidHan96.

If you want, I can also generate a compact badge row (tech stack) or add thumbnail images of each dashboard at the top.