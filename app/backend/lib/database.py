# app/backend/utils/database.py

from dataclasses import dataclass
from icecream import ic
from os.path import exists, join
from sqlite3 import connect, OperationalError, Connection, Cursor
from typing import Any, Literal

from app.backend.assets.config import DB_LOCATION, DB_MYSQL_URI_TEMPLATE, DB_POSTGRES_URI_TEMPLATE
from app.backend.assets.tables_ddl import TABLES_DDL_DEFS
from app.backend.lib.exceptions import SQLiteDatabaseException
from app.backend.utils.singletons import Singleton


@dataclass
class Database(metaclass=Singleton):
    db_uri: str
    db_type: Literal["sqlite", "mysql", "postgres"]

    def __init__(self, db_type: Literal["sqlite", "mysql", "postgres"], ) -> None:
        db_files: dict[str, str] = {
            "sqlite": join(DB_LOCATION, "prod.db"),
            "mysql": DB_MYSQL_URI_TEMPLATE,
            "postgres": DB_POSTGRES_URI_TEMPLATE,
        }
        self.db_type = db_type
        self.db_uri = db_files.get(self.db_type, "")
        if self.db_uri == "":
            raise Exception
        ic(self.db_uri)
        if self.db_type == "sqlite":
            try:
                created_db_fg: bool = self.check_sqlite_db()
            except SQLiteDatabaseException:
                raise SQLiteDatabaseException
            if not created_db_fg:
                raise SQLiteDatabaseException
        elif self.db_type == "mysql":
            raise NotImplementedError
        elif self.db_type == "postgres":
            raise NotImplementedError
        return None
    
    # common methods
    def check_connection(self) -> bool:
        if self.db_type == "sqlite":
            try:
                conn: Connection = connect(database=self.db_uri)
                conn.close()
                return True
            except OperationalError:
                return False
            except Exception:
                return False
        elif self.db_type == "mysql":
            ic("MySQL connection not implemented")
            return False
        elif self.db_type == "postgres":
            ic("PostgreSQL connection not implemented")
            return False
        else:
            raise Exception
    
    # sqlite methods
    def check_sqlite_db(self) -> bool:
        if exists(path=self.db_uri):
            print("SQLite database file exists. Proceeding...")
            return True
        else:
            print("No SQLite file found. Creating database...")
            try:
                conn: Connection = connect(database=self.db_uri)
                conn.close()
            except OperationalError as e:
                print("Something went wrong with the database creation. Check the following error stack:")
                print(e)
                raise SQLiteDatabaseException
            except Exception as e:
                print("Something went wrong while creating the database. Check the following error stack:")
                print(e)
                raise SQLiteDatabaseException
            if exists(self.db_uri):
                print("SQLite database file successfully created. Proceeding...")
                return True
            else:
                print("Something went wrong. Please review and retry.")
                return False
    
    def setup_sqlite_db(self) -> bool:
        conn: Connection = connect(database=self.db_uri)
        for ddl in TABLES_DDL_DEFS:
            ic(ddl[0], ddl[1])
            print(f"Creating table {ddl[1]}...")
            try:
                conn.execute(ddl[0])
            except OperationalError as e:
                print(f"Something went wrong with the table creation for table {ddl[1]}. Check the following error stack:")
                print(e)
                raise SQLiteDatabaseException
            except Exception as e:
                print(f"Something went wrong while creating table table {ddl[1]}. Check the following error stack:")
                print(e)
                raise SQLiteDatabaseException
        conn.close()
        return True
    
    def check_table(self, table_name: str) -> bool:
        q: str = """
        SELECT
            name
        FROM
            sqlite_schema
        WHERE
            type = "table"
            AND name NOT LIKE "sqlite_%"
        """
        conn: Connection = connect(database=self.db_uri)
        exec: Cursor = conn.execute(q)
        result: list = exec.fetchall()
        tables: list[str] = []
        for table in result:
            tables.append(table[0])
        ic(result, tables)
        if table_name in tables:
            return True
        else:
            return False

    def query(self, query_str: str) -> Any:
        return ""


def heartbeat() -> bool:
    db: Database = Database(db_type="sqlite")
    connection: bool = db.check_connection()
    return connection
