# tests/backend/test_ingestion.py

from os import getcwd
from os.path import exists, join
from pandas import DataFrame

from app.backend.assets.config import DB_TYPE
from app.backend.functions.ingest import _get_table_header, _ingest_csv_data
from app.backend.lib.database import Database


TABLE_NAME_OK: str = "jobs"
TABLE_NAME_NOK: str = "job"
JOBS_FILE_LOC: str = join(getcwd(), "app", "backend", "input", "jobs.csv")

db: Database = Database(db_type=DB_TYPE)        # type: ignore


def test_get_table_header():
    result = _get_table_header(table_name=TABLE_NAME_OK)
    assert isinstance(result, list)


def test_ingest_csv_data_file():
    if exists(path=JOBS_FILE_LOC):
        result = _ingest_csv_data(file_location=JOBS_FILE_LOC, names_list=_get_table_header(table_name=TABLE_NAME_OK), num_rows=None)
    else:
        raise Exception
    assert isinstance(result, DataFrame)
