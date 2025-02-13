# tests/backend/database.py

from app.backend.lib.database import Database


DB_TYPE: str = "sqlite"


# sqlite database tests
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


def test_heartbeat():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.heartbeat()
    assert result is True
