# app/backend/utils/database.py

from dataclasses import dataclass
from os import getcwd
from os.path import exists, join
from sqlite3 import connect, Connection
from sqlalchemy import text, column, func, table, Engine
from sqlmodel import SQLModel, Session, Table, Field, create_engine, select as select_sqlm
from traceback import print_exc
from typing import Any, Literal, Optional

from app.backend.assets.config import DB_URIS, icl
from app.backend.lib.exceptions import DatabaseException
from app.backend.utils.singletons import Singleton


# sqlmodel table classes
class HiredEmployees(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    datetime: Optional[str]
    department_id: int = Field(foreign_key="departments.id")
    job_id: int = Field(foreign_key="jobs.id")

class Departments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    department: str

class Jobs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job: str


@dataclass
class Database(metaclass=Singleton):
    db_uri: str
    db_loc: str
    db_type: Literal["sqlite", "mysql", "postgres"]
    engine: Engine

    def __init__(self, db_type: Literal["sqlite", "mysql", "postgres"], ) -> None:
        if db_type not in ["sqlite", "mysql", "postgres"]:
            raise ValueError("Database type not allowed")
        self.db_type = db_type
        self.db_uri = DB_URIS.get(self.db_type, "")
        if self.db_uri == "":
            raise Exception
        icl(self.db_uri)
        if self.db_type == "sqlite":
            # complete uri
            self.db_loc: str = join(getcwd(), "app", "backend", "db", "prod.db")
            db_uri_complete: str = f"{self.db_uri.replace("fileloc", f"/{self.db_loc}")}"
            icl(db_uri_complete)
            self.db_uri = db_uri_complete
            icl(self.db_uri)
            # create engine
            self.engine = create_engine(url=self.db_uri, echo=True)
            # setup database
            self.setup_db()
            # check database
            self.check_connection()
        elif self.db_type == "mysql":
            raise NotImplementedError
        elif self.db_type == "postgres":
            raise NotImplementedError
        print("Database successfully initialized.")
        return None
    
    def check_connection(self) -> bool:
        with self.engine.connect() as conn:
            try:
                conn.execute(text("SELECT 1"))
                return True
            except Exception as e:
                print("An exception occurred:")
                icl(e)
                print_exc()
                raise DatabaseException
    
    def setup_db(self) -> None:
        icl(self.db_uri, self.db_loc, self.db_type, self.engine)
        if self.db_type == "sqlite":
            if not exists(self.db_loc):
                print("SQLite database file not found. Creating db file...")
                conn: Connection = connect(database=self.db_loc)
                conn.close()
            else:
                print("SQLite database file found. Proceeding...")
        try:
            SQLModel.metadata.create_all(bind=self.engine, checkfirst=True)
        except Exception as e:
            print("An exception occurred:")
            icl(e)
            print_exc()
            raise DatabaseException
        return None
    
    def check_table(self, table_name: str) -> bool:
        icl(SQLModel.metadata.tables, SQLModel.metadata.tables.keys())
        tables: list[Any] = SQLModel.metadata.tables.keys()     # type: ignore
        icl(tables)
        if table_name in tables:
            return True
        else:
            return False
    
    def get_tables(self) -> list[str]:
        tables: list[Any] = SQLModel.metadata.tables.keys()     # type: ignore
        existing_tables: list[str] = []
        for table in tables:
            icl(table)
            existing_tables.append(table)
        icl(existing_tables)
        return existing_tables
    
    def get_row_cnt(self, table_name: str) -> int:
        target_table: Optional[Table] = SQLModel.metadata.tables.get(table_name)
        if target_table is None:
            raise ValueError
        with Session(self.engine) as session:
            query_table = table(table_name, column("id"))
            query = select_sqlm(func.count()).select_from(query_table)
            count = session.exec(query).all()
        icl(count, type(count))
        return count[0]

    def query(self, query_str: str) -> Any:
        return ""
    
    def heartbeat(self) -> bool:
        return self.check_connection()
