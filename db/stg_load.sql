-- =========================================================
-- RAW → STG Transformation
-- Database: JOBDASH
-- =========================================================

-- ======================================
-- Applications STG
-- ======================================
CREATE OR REPLACE TABLE JOBDASH.STG.JOB_APPLICATIONS_STG AS
SELECT
    -- Identifiers
    APP_ID                                 AS APP_ID,

    -- Strings
    TRIM(COMPANY)                          AS COMPANY_NAME,
    TRIM(INDUSTRY)                         AS INDUSTRY,
    TRIM(SOURCE_PLATFORM)                  AS SOURCE,
    TRIM(APPLICATION_STATUS)               AS APPLICATION_STATUS,
    TRIM(INTERVIEW_STATUS)                 AS INTERVIEW_STATUS,  -- New column
    TRIM(REFERRAL)                         AS REFERRAL,
    TRIM(ROLE_TITLE)                       AS ROLE_TITLE,
    TRIM(WORK_ARRANGEMENT)                 AS WORK_ARRANGEMENT,
    TRIM(CITY)                             AS CITY,
    TRIM(STATE)                            AS STATE,

    -- Numerics
    COMPENSATION                           AS COMPENSATION,

    -- Dates / Timestamps
    DATE_APPLIED                           AS DATE_APPLIED,
    CREATED_AT                             AS CREATED_AT,
    LAST_MODIFIED                          AS LAST_MODIFIED,

    -- Flags
    COALESCE(IS_DELETED, 'no')             AS IS_DELETED

FROM JOBDASH.RAW.JOB_APPLICATIONS_RAW;


-- ======================================
-- Study Logs STG
-- ======================================
CREATE OR REPLACE TABLE JOBDASH.STG.STUDY_LOG_STG AS
SELECT
    STUDY_ID                               AS STUDY_ID,
    TRIM(MAIN_CATEGORY)                    AS MAIN_CATEGORY,
    TRIM(SUB_CATEGORY)                     AS SUB_CATEGORY,
    TRIM(TOPIC)                            AS TOPIC,
    TRIM(PROVIDER)                         AS PROVIDER,
    TRIM(DIFFICULTY)                       AS DIFFICULTY,
    PROBLEMS_SOLVED                        AS PROBLEMS_SOLVED,
    HOURS                                  AS HOURS,
    SESSION_DATE                           AS SESSION_DATE,
    CREATED_AT                             AS CREATED_AT
FROM JOBDASH.RAW.STUDY_LOG_RAW;
