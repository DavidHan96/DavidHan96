# Study Log Analytics Dashboard

Google Looker Studio dashboard powered by Snowflake.

👉 [View Interactive Dashboard](https://lookerstudio.google.com/reporting/edeb330e-5a46-4eda-b1e1-1941c14eb872)

---

## Features
- Daily study hours with 7-day moving average
- Problems solved tracking with rolling average
- Category share of study hours (donut chart)
- Smart ranking of categories (hours, problems, difficulty)
- Session-level details table with filters

---

## Data Pipeline
- **Source**: Google Sheets  
- **Warehouse**: Snowflake (RAW → STG → FACT → VIEW)  
- **Visualization**: Looker Studio  

---

## Preview
📄 Exported PDF: [Study_Log_Analytics.pdf](Study_Log_Analytics.pdf)
