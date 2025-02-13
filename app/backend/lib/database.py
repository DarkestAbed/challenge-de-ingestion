# app/backend/utils/database.py

from dataclasses import dataclass
from icecream import ic
from os import getcwd
from os.path import exists, join
from sqlite3 import connect, OperationalError, Connection, Cursor
from sqlalchemy import Engine
from sqlmodel import SQLModel, Field, create_engine
from typing import Any, Literal, Optional

from app.backend.assets.config import DB_URIS
from app.backend.assets.tables_ddl import TABLES_DDL_DEFS, TABLES
from app.backend.lib.exceptions import SQLiteDatabaseException
from app.backend.utils.singletons import Singleton


@dataclass
class Database(metaclass=Singleton):
    db_uri: str
    db_type: Literal["sqlite", "mysql", "postgres"]
    engine: Engine

    def __init__(self, db_type: Literal["sqlite", "mysql", "postgres"], ) -> None:
        if db_type not in ["sqlite", "mysql", "postgres"]:
            raise ValueError("Database type not allowed")
        self.db_type = db_type
        self.db_uri = DB_URIS.get(self.db_type, "")
        if self.db_uri == "":
            raise Exception
        ic(self.db_uri)
        if self.db_type == "sqlite":
            # complete uri
            db_uri_complete: str = f"{self.db_uri}"
            # check database
            # try:
            #     created_db_fg: bool = self.check_sqlite_db()
            # except SQLiteDatabaseException:
            #     raise SQLiteDatabaseException
            # if not created_db_fg:
            #     raise SQLiteDatabaseException
            # setup database
            # Database.setup_init()
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
    
    # sqlmodel tables subclasses
    class HiredEmployees(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        datetime: str
        department_id: int
        job_id: int
    
    class Departments(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        department: str
    
    class Jobs(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        job: str
    
    # sqlite methods
    def check_db(self) -> bool:
        return True
    
    def setup_db(self) -> bool:
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

    @staticmethod
    def heartbeat() -> bool:
        db: Database = Database(db_type="sqlite")
        connection: bool = db.check_connection()
        return connection
