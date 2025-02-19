# app/backend/reports/employees_by_quarter.py

from pandas import DataFrame

from app.backend.assets.config import DB_TYPE
from app.backend.lib.database import Database


db: Database = Database(db_type=DB_TYPE)        # type: ignore


def get_employees_by_quarter() -> DataFrame:
    query: str = """
    WITH
    wide_table AS
    (
        SELECT
            he.id
            ,he.datetime
            ,he.department_id
            ,d.department
            ,he.job_id
            ,j.job
        FROM
            hiredemployees AS he
        LEFT JOIN
            departments AS d
            ON he.department_id = d.id
        LEFT JOIN
            jobs AS j
            ON he.job_id = j.id
        WHERE
            he.datetime >= '2021-01-01 00:00:00'
            AND he.datetime < '2022-01-01 00:00:00'
    ),
    quarter_added AS
    (
        SELECT
            id
            ,department
            ,job
            ,datetime
            ,SUBSTR(datetime, 6, 2) AS month_date
            ,CASE 
                WHEN 0 + STRFTIME('%m', datetime) BETWEEN  1 AND  3 THEN 'Q1'
                WHEN 0 + STRFTIME('%m', datetime) BETWEEN  4 AND  6 THEN 'Q2'
                WHEN 0 + STRFTIME('%m', datetime) BETWEEN  7 AND  9 THEN 'Q3'
                WHEN 0 + STRFTIME('%m', datetime) BETWEEN 10 AND 12 THEN 'Q4'
            END AS quarter
        FROM
            wide_table
        WHERE
            department IS NOT NULL
            AND job IS NOT NULL
    )

    SELECT
        department
        ,job
        ,SUM(CASE WHEN quarter = 'Q1' THEN 1 ELSE 0 END) AS Q1
        ,SUM(CASE WHEN quarter = 'Q2' THEN 1 ELSE 0 END) AS Q2
        ,SUM(CASE WHEN quarter = 'Q3' THEN 1 ELSE 0 END) AS Q3
        ,SUM(CASE WHEN quarter = 'Q4' THEN 1 ELSE 0 END) AS Q4
    FROM
        quarter_added
    GROUP BY
        department
        ,job
    ORDER BY
        department ASC
        ,job ASC
    """
    results: DataFrame = db.query(query_str=query)
    return results
