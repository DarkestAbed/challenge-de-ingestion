# app/backend/utils/database.py

from dataclasses import dataclass
from icecream import ic
from os.path import exists, join
from sqlite3 import connect, OperationalError
from typing import Literal

from app.backend.assets.config import DB_LOCATION
from app.backend.lib.exceptions import SQLiteDatabaseException


@dataclass
class Database:
    db_uri: str
    db_type: Literal["sqlite", "mysql", "postgres"] = "sqlite"

    def __init__(self, db_type: Literal["sqlite", "mysql", "postgres"], ) -> None:
        db_files: dict[str] = {
            "sqlite": join(DB_LOCATION, "prod.db"),
            "mysql": "",
            "postgres": "",
        }
        self.db_type: str = db_type
        self.db_uri: str = db_files.get(self.db_typedb_type)
        ic(self.db_uri)
        if self.db_type == "sqlite":
            created_db_fg: bool = self.check_sqlite_db()
        elif self.db_type == "mysql":
            raise NotImplementedError
        elif self.db_type == "postgres":
            raise NotImplementedError
        return None
    
    def check_sqlite_db(self) -> bool:
        if exists(self.db_uri):
            print("SQLite database file exists. Proceeding...")
        else:
            print("No SQLite file found. Creating database...")
            try:
                connect(database=self.db_uri)
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
