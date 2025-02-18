# tests/backend/database.py
"""
The tests are tailored to a SQLite experience. However, extensibility is possible using SQLModel and SQLAlchemy packages.
# TODO:
Implement functionality for a MySQL and a PostgreSQL database
"""

from app.backend.assets.config import DB_TYPE
from app.backend.lib.database import Database


TABLE_NAME: str = "jobs"


def test_create_sqlite_db_object():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    assert isinstance(db, Database)


def test_check_sqlite_db_file():
    from os.path import exists
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    assert exists(db.db_loc) is True


def test_check_sqlite_db_connection():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.check_connection()
    assert result is True


def test_check_sqlite_db_tables():
    from app.backend.assets.tables import TABLES
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    cnt_tables: int = 0
    for table in TABLES:
        check: bool = db.check_table(table_name=table)
        if check:
            cnt_tables += 1
    assert cnt_tables == 3


def test_get_sqlite_db_tables():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.get_tables()
    assert isinstance(result, list)


def test_get_row_num_on_table():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.get_row_cnt(table_name=TABLE_NAME)
    assert isinstance(result, int) and result >= 0


def test_heartbeat():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.heartbeat()
    assert result is True
