# app/backend/functions/automated_etl.py

from os import remove
from os.path import exists, join
from pandas import DataFrame
from time import sleep
from traceback import print_exc

from app.backend.assets.config import DB_TYPE, INPUT_LOCATION, icl
from app.backend.lib.database import Database
from app.backend.functions.ingest import _get_table_header, _ingest_csv_data
from app.backend.functions.load import load_data_into_db, dedupe_data_on_table


FILES_TO_LOAD: list[str] = ["jobs", "departments", "hired_employees"]
CONTROL_FILE: str = join(INPUT_LOCATION, ".process")

db: Database = Database(db_type=DB_TYPE)        # type: ignore


def start_process() -> None:
    if exists(CONTROL_FILE):
        raise RuntimeError
    with open(file=CONTROL_FILE, mode="w") as f:
        string: str = "PROCESSING"
        f.write(string)
    return None


def check_process() -> bool:
    if exists(CONTROL_FILE):
        return False
    else:
        return True
    

def finish_process() -> None:
    remove(path=CONTROL_FILE)
    return None


def extract(file_name: str, table_name: str) -> DataFrame:
    FILE_LOC: str = join(INPUT_LOCATION, f"{file_name}.csv")
    icl(FILE_LOC)
    if not exists(path=FILE_LOC):
        raise FileNotFoundError
    names_list: list[str] = _get_table_header(table_name=table_name)
    data: DataFrame = _ingest_csv_data(file_location=FILE_LOC, names_list=names_list, num_rows=None)
    return data


def transform(table_data: DataFrame) -> DataFrame:
    # COMMENT: if any transformation steps were needed at a alater stage, and to improve code clarity, they should be implemented
    # here as a separate step, for conceptual clarity and maintenance
    return table_data


def load(table_data: DataFrame, table_name: str):
    num_rows_added: int = load_data_into_db(table_pd=table_data, table_name=table_name)
    _ = dedupe_data_on_table(table_name=table_name)
    return num_rows_added


def etl():
    start_process()
    for file in FILES_TO_LOAD:
        icl(file)
        table: str = file.replace("_", "")
        try:
            raw_data: DataFrame = extract(file_name=file, table_name=table)
            transformed_data: DataFrame = transform(table_data=raw_data)
            final_rows: int = load(table_data=transformed_data, table_name=table)
            print(f"Uploaded {final_rows} rows to the table {file}")
        except RuntimeError:
            print("A previous ETL process is running.")
            raise RuntimeError
        except Exception as e:
            icl(e)
            print_exc()
            print("Something happened during the load process. Please review and retry.")
            raise Exception
        sleep(5)
    finish_process()
    return None
