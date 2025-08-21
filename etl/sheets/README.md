# Google Sheets Incremental Load Script

This folder contains Apps Script code used in Google Sheets 
(`job_applicants`, `study_logs`) to simulate audit columns and support incremental loads.

## Features
- Auto-increment IDs: `app_id`, `study_id`
- `created_at`: Set once when a new row is inserted
- `last_modified`: Updated automatically on every edit

## Why
This ensures every row has proper audit columns, so data can be ingested 
incrementally into Snowflake or another data warehouse.

## Usage in ETL
Example incremental load query:

```sql
SELECT *
FROM job_applicants
WHERE last_modified > '{{ last_run_time }}';
