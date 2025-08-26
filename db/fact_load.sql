-- =========================================================
-- FACT LOAD SCRIPT
-- Load data from STG tables into FACT tables
-- Database: JOBDASH.ANALYTICS
-- =========================================================

-- ======================================
-- FACT: Job Applications
-- ======================================
CREATE OR REPLACE TABLE JOBDASH.ANALYTICS.FACT_JOB_APPLICATION AS
SELECT
    ROW_NUMBER() OVER (ORDER BY a.APP_ID)        AS APPLICATION_KEY,
    a.APP_ID                                     AS APP_ID,

    -- Dimension lookups
    c.COMPANY_KEY                                AS COMPANY_KEY,
    r.ROLE_KEY                                   AS ROLE_KEY,
    w.WORK_KEY                                   AS WORK_KEY,
    l.LOCATION_KEY                               AS LOCATION_KEY,
    s.SOURCE_KEY                                 AS SOURCE_KEY,

    -- Dates
    d1.DATE_KEY                                  AS APPLIED_DATE_KEY,
    d2.DATE_KEY                                  AS LAST_MODIFIED_DATE_KEY,

    -- Attributes
    a.APPLICATION_STATUS                         AS STATUS,
    a.INTERVIEW_STATUS                           AS INTERVIEW_STATUS,
    a.REFERRAL                                   AS REFERRAL,
    a.COMPENSATION                               AS COMPENSATION,
    a.IS_DELETED                                 AS IS_DELETED,

    -- Audit
    a.CREATED_AT                                 AS CREATED_AT

FROM JOBDASH.STG.JOB_APPLICATIONS_STG a
LEFT JOIN JOBDASH.ANALYTICS.DIM_COMPANY c
    ON a.COMPANY_NAME = c.COMPANY_NAME
LEFT JOIN JOBDASH.ANALYTICS.DIM_ROLE r
    ON a.ROLE_TITLE = r.ROLE_TITLE
LEFT JOIN JOBDASH.ANALYTICS.DIM_WORK_ARRANGEMENT w
    ON a.WORK_ARRANGEMENT = w.WORK_ARRANGEMENT
LEFT JOIN JOBDASH.ANALYTICS.DIM_LOCATION l
    ON a.CITY = l.CITY
   AND a.STATE = l.STATE
LEFT JOIN JOBDASH.ANALYTICS.DIM_SOURCE s
    ON a.SOURCE = s.SOURCE_NAME
LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d1
    ON a.DATE_APPLIED = d1.FULL_DATE
LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d2
    ON a.LAST_MODIFIED = d2.FULL_DATE;

-- ======================================
-- FACT: Study Sessions
-- ======================================
CREATE OR REPLACE TABLE JOBDASH.ANALYTICS.FACT_STUDY_SESSIONS AS
SELECT
    ROW_NUMBER() OVER (ORDER BY s.STUDY_ID)      AS SESSION_KEY,
    s.STUDY_ID                                   AS STUDY_ID,

    -- Dimension lookups
    t.TOPIC_KEY                                  AS TOPIC_KEY,
    p.PROVIDER_KEY                               AS PROVIDER_KEY,
    d.DATE_KEY                                   AS SESSION_DATE_KEY,

    -- Measures & attributes
    s.PROBLEMS_SOLVED                            AS PROBLEMS_SOLVED,
    s.HOURS                                      AS HOURS,
    s.DIFFICULTY                                 AS DIFFICULTY,

    -- Audit
    s.CREATED_AT                                 AS CREATED_AT

FROM JOBDASH.STG.STUDY_LOG_STG s
LEFT JOIN JOBDASH.ANALYTICS.DIM_TOPIC t 
    ON s.TOPIC = t.TOPIC
LEFT JOIN JOBDASH.ANALYTICS.DIM_PROVIDER p 
    ON s.PROVIDER = p.PROVIDER_NAME   -- ✅ fixed to match actual DIM_PROVIDER design
LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d 
    ON s.SESSION_DATE = d.FULL_DATE;
