-- ====================================
-- CREATE ALL TABLES (DIM + FACT + RAW + STG)
-- ====================================

-- Run this file to build entire schema at once

-- DIMENSIONS
@@dim_tables.sql

-- FACTS
@@fact_tables.sql

-- RAW
@@raw_tables.sql

-- STAGING
@@stg_tables.sql
