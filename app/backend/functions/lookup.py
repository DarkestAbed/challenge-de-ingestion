# app/backend/functions/lookup.py

from sqlmodel import select, Session
from typing import Any

from app.backend.assets.config import DB_TYPE, icl
from app.backend.assets.tables import TABLES_OBJ
from app.backend.lib.database import Database


db: Database = Database(db_type=DB_TYPE)        # type: ignore


def get_data_snippet(table_name: str) -> Any | bool:
    table: Any = TABLES_OBJ.get(table_name)
    with Session(db.engine) as session:
        query: Any = select(table).limit(10)
        results: Any = session.exec(query).all()
        icl(results)
    if len(results) == 0:
        return False
    else:
        return results
