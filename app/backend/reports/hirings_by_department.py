# app/backend/reports/hirings_by_department.py

from pandas import DataFrame

from app.backend.assets.config import DB_TYPE
from app.backend.lib.database import Database


db: Database = Database(db_type=DB_TYPE)        # type: ignore


def get_mean_hires(year: int) -> DataFrame:
    query: str = f"""
    WITH
    wide_table AS
    (
        SELECT
            he.id
            ,he.department_id
            ,d.department
        FROM
            hiredemployees AS he
        LEFT JOIN
            departments AS d
            ON he.department_id = d.id
        WHERE
            datetime >= '{year}-01-01 00:00:00'
            AND datetime < '{year + 1}-01-01 00:00:00'
    ),
    department_hires AS
    (
        SELECT
            department_id
            ,department
            ,COUNT(id) AS hires
        FROM
            wide_table
        GROUP BY
            department_id
    )

    SELECT
        ROUND(AVG(hires), 0) AS mean_hires
    FROM
        department_hires
    """
    result = db.query(query_str=query)
    return result


def get_departments_over_mean() -> DataFrame:
    query: str = """
    WITH
    wide_table AS
    (
        SELECT
            he.id
            ,he.department_id
            ,d.department
        FROM
            hiredemployees AS he
        LEFT JOIN
            departments AS d
            ON he.department_id = d.id
        WHERE
            datetime >= '2021-01-01 00:00:00'
            AND datetime < '2022-01-01 00:00:00'
    ),
    department_hires AS
    (
        SELECT
            department_id
            ,department
            ,COUNT(id) AS hires
        FROM
            wide_table
        GROUP BY
            department_id
            ,department
    ),
    departments_over_mean AS
    (
        SELECT
            department_id
            ,department
            ,COUNT(id) AS hires
        FROM
            wide_table
        GROUP BY
            department_id
            ,department
        HAVING
            COUNT(id) > (SELECT ROUND(AVG(hires), 0) FROM department_hires)
    )

    SELECT
        department_id
        ,department
        ,hires
    FROM
        departments_over_mean
    ORDER BY
        hires DESC
    """
    result: DataFrame = db.query(query_str=query)
    return result