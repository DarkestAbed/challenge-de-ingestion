# tests/backend/database.py

from app.backend.lib.database import Database, heartbeat, setup_init


DB_TYPE: str = "sqlite"


# sqlite database tests
def test_create_sqlite_db_object():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    assert isinstance(db, Database)


def test_check_sqlite_db_file():
    from os.path import exists, join
    from app.backend.assets.config import DB_LOCATION
    db_file: str = join(DB_LOCATION, "prod.db")
    _: Database = Database(db_type=DB_TYPE)        # type: ignore
    assert exists(db_file) is True


def test_check_sqlite_db_connection():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.check_connection()
    assert result is True


def test_setup_sqlite_db():
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    result = db.setup_sqlite_db()
    assert result is True


def test_check_sqlite_db_tables():
    TABLES_LIST: list[str] = ["departments", "hired_employees", "jobs"]
    db: Database = Database(db_type=DB_TYPE)        # type: ignore
    cnt_tables: int = 0
    for table in TABLES_LIST:
        check: bool = db.check_table(table_name=table)
        if check:
            cnt_tables += 1
    assert cnt_tables == 3


def test_heartbeat():
    result = heartbeat()
    assert result is True


def test_startup_setup():
    result = setup_init()
    assert result is None
