-- =========================================================
-- RAW → STG Transformation
-- Database: JOBDASH
-- =========================================================

-- ======================================
-- Applications STG (incremental with last_modified)
-- ======================================
CREATE OR REPLACE TABLE JOBDASH.STG.JOB_APPLICATIONS_STG AS
SELECT
    -- Identifiers
    APP_ID                           AS APP_ID,

    -- Strings
    TRIM(COMPANY)                    AS COMPANY_NAME,
    TRIM(INDUSTRY)                   AS INDUSTRY,
    TRIM(SOURCE_PLATFORM)            AS SOURCE,
    TRIM(APPLICATION_STATUS)         AS APPLICATION_STATUS,
    TRIM(REFERRAL)                   AS REFERRAL,
    TRIM(ROLE_TITLE)                 AS ROLE_TITLE,
    TRIM(WORK_ARRANGEMENT)           AS WORK_ARRANGEMENT,
    TRIM(CITY)                       AS CITY,
    TRIM(STATE)                      AS STATE,

    -- Numerics
    COMPENSATION                     AS COMPENSATION,

    -- Dates / Timestamps
    DATE_APPLIED                     AS DATE_APPLIED,
    CREATED_AT                       AS CREATED_AT,
    LAST_MODIFIED                    AS LAST_MODIFIED,   -- required for incremental

    -- Flags
    COALESCE(IS_DELETED, 'no')       AS IS_DELETED

FROM JOBDASH.RAW.JOB_APPLICATIONS_RAW;


-- ======================================
-- Study Logs STG (append-only, no last_modified)
-- ======================================
CREATE OR REPLACE TABLE JOBDASH.STG.STUDY_LOG_STG AS
SELECT
    -- Identifiers
    STUDY_ID                         AS STUDY_ID,

    -- Strings
    TRIM(MAIN_CATEGORY)              AS MAIN_CATEGORY,
    TRIM(SUB_CATEGORY)               AS SUB_CATEGORY,
    TRIM(TOPIC)                      AS TOPIC,
    TRIM(PROVIDER)                   AS PROVIDER,
    TRIM(DIFFICULTY)                 AS DIFFICULTY,

    -- Numerics
    PROBLEMS_SOLVED                  AS PROBLEMS_SOLVED,
    HOURS                            AS HOURS,

    -- Dates / Timestamps
    SESSION_DATE                     AS SESSION_DATE,
    CREATED_AT                       AS CREATED_AT       -- no last_modified here

FROM JOBDASH.RAW.STUDY_LOG_RAW;
