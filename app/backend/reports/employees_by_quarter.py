# app/backend/reports/employees_by_quarter.py

from pandas import DataFrame

from app.backend.assets.config import DB_TYPE
from app.backend.lib.database import Database


db: Database = Database(db_type=DB_TYPE)        # type: ignore


def compile_query():
    return None


def execute_query():
    return None


def deliver_results():
    return None
