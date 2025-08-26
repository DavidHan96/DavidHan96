# Google Sheets → Snowflake ETL

This folder contains all code required to load data from Google Sheets into Snowflake,
supporting both full initial loads and incremental upserts.

---

## Files

- **load_initial.py**  
  - Truncates the RAW tables and reloads all rows from Google Sheets.
  - Normalizes column types (dates, timestamps, numerics, booleans).
  - Use this when setting up a new environment or resyncing all data.

- **incremental_load.py**  
  - Reads only rows that are new or modified (based on `last_modified`).
  - Performs MERGE for `applications` (update or insert).
  - Performs append/insert for `study_logs`.
  - Intended for daily/recurring runs.

- **incremental_load.gs**  
  - Google Apps Script that auto-fills `app_id` / `study_id`, `created_at`, `last_modified`.
  - Ensures audit columns are always present in Google Sheets.

---

## Features

- Auto-increment IDs (`app_id`, `study_id`) handled in Apps Script.
- Audit columns:
  - `created_at`: set once when a row is first created.
  - `last_modified`: updated automatically on every edit.
- Serial date values from Google Sheets handled safely (converted to ISO).
- Timestamps stored in Snowflake as `TIMESTAMP_NTZ(3)` for millisecond precision.

---

## Usage

### Initial load (one-time or full reload)
```bash
py -3.13 etl/sheets/load_initial.py
