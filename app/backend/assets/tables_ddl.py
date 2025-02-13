# app/backend/asserts/tables_ddl.py

TABLES: list[str] = ["hired_employees", "departments", "jobs"]
HIRED_EMPLOYEES: str = """
CREATE TABLE IF NOT EXISTS
    hired_employees
    (
        id INTEGER PRIMARY KEY
        ,name STRING
        ,datetime STRING
        ,department_id INTEGER
        ,job_id INTEGER
    )
;
"""
DEPARTMENTS: str = """
CREATE TABLE IF NOT EXISTS
    departments
    (
        id INTEGER PRIMARY KEY
        ,department STRING
    )
;
"""
JOBS: str = """
CREATE TABLE IF NOT EXISTS
    jobs
    (
        id INTEGER PRIMARY KEY
        ,job STRING
    )
;
"""
TABLES_DDL_DEFS: list[tuple] = [(HIRED_EMPLOYEES, "hired_employees"), (DEPARTMENTS, "departments"), (JOBS, "jobs")]
