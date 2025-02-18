# tests/backend/test_load.py

from os import getcwd
from os.path import join
from pandas import DataFrame

from app.backend.assets.config import DB_TYPE
from app.backend.functions.load import load_data_into_db, dedupe_data_on_table
from app.backend.functions.ingest import _ingest_csv_data, _get_table_header
from app.backend.lib.database import Database


db: Database = Database(db_type=DB_TYPE)        # type: ignore
TABLE_NAME: str = "jobs"
JOBS_FILE_LOC: str = join(getcwd(), "app", "backend", "input", "jobs.csv")


def test_load_data_into_db():
    db.check_table(table_name=TABLE_NAME)
    names: list[str] = _get_table_header(table_name=TABLE_NAME)
    data: DataFrame = _ingest_csv_data(file_location=JOBS_FILE_LOC, names_list=names, num_rows=None)
    additional_rows: int = data.shape[0]
    final_count: int = load_data_into_db(table_pd=data, table_name=TABLE_NAME)
    assert (additional_rows == final_count)


def test_deduplicate_data():
    db.check_table(table_name=TABLE_NAME)
    names: list[str] = _get_table_header(table_name=TABLE_NAME)
    data: DataFrame = _ingest_csv_data(file_location=JOBS_FILE_LOC, names_list=names, num_rows=None)
    additional_rows: int = data.shape[0]
    dedupe_data_on_table(table_name=TABLE_NAME)
    final_rows: int = db.get_row_cnt(table_name=TABLE_NAME)
    assert (additional_rows == final_rows)
    assert True is True
