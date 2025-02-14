# app/backend/functions/load.py

from pandas import DataFrame, read_sql_table
from typing import Optional

from app.backend.assets.config import DB_TYPE, icl
from app.backend.lib.database import Database
from app.backend.lib.exceptions import DatabaseException, InsertException


db: Database = Database(db_type=DB_TYPE)        # type: ignore


def load_data_into_db(table_pd: DataFrame, table_name: str) -> int:
    try:
        affected_rows: Optional[int] = table_pd.to_sql(name=table_name, con=db.engine, if_exists="append", index=False, method=None)
    except Exception as e:
        print("An error ocurred while loading data into database.")
        icl(e)
        raise InsertException
    return affected_rows        # type: ignore


def dedupe_data_on_table(table_name: str):
    current_data: DataFrame = read_sql_table(table_name=table_name, con=db.engine)
    # get columns to check for duplicated values
    data_cols: list[str] = current_data.columns     # type: ignore
    subset_cols: list[str] = []
    icl(data_cols)
    for col in data_cols:
        if not col == "id":
            subset_cols.append(col)
    icl(subset_cols)
    # dedupe data
    deduped_data: DataFrame = current_data.drop_duplicates(subset=subset_cols, keep="first", inplace=False)
    try:
        deduped_data.to_sql(name=table_name, con=db.engine, if_exists="replace", index=False)
    except Exception as e:
        print("An error ocurred while loading data into database.")
        icl(e)
        raise DatabaseException
    return None
