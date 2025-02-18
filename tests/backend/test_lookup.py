# tests/backend/test_load.py

from os import getcwd
from os.path import join
from pandas import DataFrame

from app.backend.assets.config import DB_TYPE, icl
from app.backend.functions.lookup import get_data_snippet
from app.backend.lib.database import Database


db: Database = Database(db_type=DB_TYPE)        # type: ignore
TABLE_NAME: str = "jobs"


def test_get_data_snippet():
    snippet = get_data_snippet(table_name=TABLE_NAME)
    icl(snippet, len(snippet))      # type: ignore
    assert len(snippet) <= 10       # type: ignore
