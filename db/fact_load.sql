-- =========================================================
-- FACT LOAD SCRIPT
-- Database: JOBDASH.ANALYTICS
-- =========================================================

-- =========================================================
-- FACT: Job Applications
-- =========================================================
CREATE OR REPLACE TABLE JOBDASH.ANALYTICS.FACT_JOB_APPLICATION AS
WITH base AS (
  SELECT
    a.APP_ID,
    a.APPLICATION_STATUS,
    a.INTERVIEW_STATUS,
    a.REFERRAL,
    a.COMPENSATION,
    a.IS_DELETED,
    a.CREATED_AT,
    a.COMPANY_NAME,
    a.INDUSTRY,
    a.ROLE_TITLE,
    a.WORK_ARRANGEMENT,
    a.CITY,
    a.STATE,
    a.SOURCE,
    a.DATE_APPLIED,
    a.LAST_MODIFIED
  FROM JOBDASH.STG.JOB_APPLICATIONS_STG a
),

joined AS (
  SELECT
    b.APP_ID,

    -- Dimension lookups
    c.COMPANY_KEY,
    r.ROLE_KEY,
    w.WORK_KEY,
    l.LOCATION_KEY,
    s.SOURCE_KEY,
    d1.DATE_KEY AS APPLIED_DATE_KEY,
    d2.DATE_KEY AS LAST_MODIFIED_DATE_KEY,

    -- Attributes
    b.APPLICATION_STATUS,
    b.INTERVIEW_STATUS,
    b.REFERRAL,
    b.COMPENSATION,
    b.IS_DELETED,
    b.CREATED_AT

  FROM base b
  LEFT JOIN JOBDASH.ANALYTICS.DIM_COMPANY c
    ON b.COMPANY_NAME = c.COMPANY_NAME
   AND b.INDUSTRY     = c.INDUSTRY
  LEFT JOIN JOBDASH.ANALYTICS.DIM_ROLE r
    ON b.ROLE_TITLE = r.ROLE_TITLE
  LEFT JOIN JOBDASH.ANALYTICS.DIM_WORK_ARRANGEMENT w
    ON b.WORK_ARRANGEMENT = w.WORK_ARRANGEMENT
  LEFT JOIN JOBDASH.ANALYTICS.DIM_LOCATION l
    ON b.CITY  = l.CITY
   AND b.STATE = l.STATE
  LEFT JOIN JOBDASH.ANALYTICS.DIM_SOURCE s
    ON b.SOURCE = s.SOURCE_NAME
  LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d1
    ON b.DATE_APPLIED = d1.FULL_DATE
  LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d2
    ON b.LAST_MODIFIED = d2.FULL_DATE

  -- Guarantee 1 row per APP_ID (latest by last_modified/created_at)
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY b.APP_ID
    ORDER BY b.LAST_MODIFIED NULLS LAST, b.CREATED_AT DESC
  ) = 1
)

SELECT
  ROW_NUMBER() OVER (ORDER BY APP_ID) AS APPLICATION_KEY,
  APP_ID,
  COMPANY_KEY,
  ROLE_KEY,
  WORK_KEY,
  LOCATION_KEY,
  SOURCE_KEY,
  APPLIED_DATE_KEY,
  LAST_MODIFIED_DATE_KEY,
  APPLICATION_STATUS,
  INTERVIEW_STATUS,
  REFERRAL,
  COMPENSATION,
  IS_DELETED,
  CREATED_AT
FROM joined;


-- =========================================================
-- FACT: Study Sessions
-- =========================================================
CREATE OR REPLACE TABLE JOBDASH.ANALYTICS.FACT_STUDY_SESSIONS AS
SELECT
    ROW_NUMBER() OVER (ORDER BY r.study_id) AS session_key,
    r.study_id,
    t.topic_key,
    p.provider_key,
    d.date_key AS session_date_key,
    r.problems_solved,
    r.hours,
    -- ✅ hours_per_problem with safe division
    CASE 
        WHEN r.problems_solved IS NULL OR r.problems_solved = 0 THEN 0
        ELSE r.hours / r.problems_solved
    END AS hours_per_problem,
    r.difficulty,
    r.created_at
FROM JOBDASH.STG.STUDY_LOG_STG r
LEFT JOIN JOBDASH.ANALYTICS.DIM_TOPIC t
    ON upper(trim(r.main_category)) = upper(trim(t.main_category))
   AND upper(trim(r.sub_category)) = upper(trim(t.sub_category))
   AND upper(trim(r.topic)) = upper(trim(t.topic))
LEFT JOIN JOBDASH.ANALYTICS.DIM_PROVIDER p
    ON upper(trim(r.provider)) = upper(trim(p.provider_name))
LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d
    ON r.session_date = d.full_date
WHERE r.study_id IS NOT NULL;
