CREATE OR REPLACE VIEW JOBDASH.ANALYTICS.VW_STUDY_LOG (
    SESSION_KEY,
    STUDY_ID,
    SESSION_DATE,
    WEEK_OF_YEAR,
    MONTH,
    QUARTER,
    YEAR,
    MAIN_CATEGORY,
    SUB_CATEGORY,
    TOPIC_NAME,
    PROVIDER_NAME,
    PROBLEMS_SOLVED,
    HOURS,
    HOURS_PER_PROBLEM,
    DIFFICULTY,
    DIFFICULTY_SCORE,
    IS_PROJECT,
    PROJECT_HOURS,
    CREATED_AT,
    CATEGORY_SHARE,
    ROLLING_7D_AVG_HOURS,
    ROLLING_7D_AVG_PROBLEMS
) AS
WITH base AS (
    SELECT 
        f.session_key,
        f.study_id,
        d.full_date                 AS session_date,
        d.week_of_year,
        d.month,
        d.quarter,
        d.year,

        -- Topic/Category
        t.main_category,
        t.sub_category,
        t.topic                     AS topic_name,
        p.provider_name,

        -- Study metrics
        f.problems_solved,
        f.hours,
        CASE 
            WHEN f.problems_solved > 0 THEN ROUND(f.hours / f.problems_solved, 2) 
            ELSE 0
        END                         AS hours_per_problem,

        -- Difficulty mapping
        f.difficulty,
        CASE f.difficulty
            WHEN 'Easy'   THEN 1
            WHEN 'Medium' THEN 2
            WHEN 'Hard'   THEN 3
            ELSE NULL
        END                         AS difficulty_score,

        -- Project flag
        CASE 
            WHEN t.sub_category ILIKE 'Project%' THEN 1 
            ELSE 0 
        END                         AS is_project,

        -- Project hours
        CASE 
            WHEN t.sub_category ILIKE 'Project%' THEN f.hours 
            ELSE 0 
        END                         AS project_hours,

        -- Metadata
        f.created_at
    FROM JOBDASH.ANALYTICS.FACT_STUDY_SESSIONS f
    LEFT JOIN JOBDASH.ANALYTICS.DIM_TOPIC t
        ON f.topic_key = t.topic_key
    LEFT JOIN JOBDASH.ANALYTICS.DIM_PROVIDER p
        ON f.provider_key = p.provider_key
    LEFT JOIN JOBDASH.ANALYTICS.DIM_DATE d
        ON f.session_date_key = d.date_key
),
agg AS (
    SELECT
        main_category,
        SUM(hours) AS total_hours
    FROM base
    GROUP BY main_category
),
share AS (
    SELECT
        main_category,
        ROUND(100.0 * total_hours / SUM(total_hours) OVER (), 1) AS pct_hours
    FROM agg
)
SELECT 
    b.*,
    CONCAT(b.main_category, ' (', s.pct_hours, '%)') AS category_share,

    -- Rolling 7-day average for study hours (based on session_date order)
    ROUND(
        AVG(b.hours) OVER (
            ORDER BY b.session_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_7d_avg_hours,

    -- Rolling 7-day average for problems solved
    ROUND(
        AVG(b.problems_solved) OVER (
            ORDER BY b.session_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_7d_avg_problems

FROM base b
LEFT JOIN share s
    ON b.main_category = s.main_category;
