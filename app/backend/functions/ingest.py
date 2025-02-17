# app/backend/functions/ingest.py

from fastapi import UploadFile
from os.path import join
from pandas import DataFrame, read_csv
from sqlmodel import SQLModel, Table
from typing import Optional
from uuid import uuid4

from app.backend.assets.config import OUTPUT_LOCATION, icl
from app.backend.lib.exceptions import UploadException


def _get_table_header(table_name: str) -> list[str]:
    table_metadata: Optional[Table] = SQLModel.metadata.tables.get(table_name)
    if table_metadata is None:
        raise ValueError
    icl(table_metadata.columns.keys())
    return table_metadata.columns.keys()


def _ingest_csv_data(file_location: str, names_list: list[str], num_rows: Optional[int]) -> DataFrame:
    if num_rows is None:
        ingest_pd: DataFrame = read_csv(filepath_or_buffer=file_location, sep=",", header=None, names=names_list)
    elif isinstance(num_rows, int) and num_rows > 0 and num_rows <= 1000:
        ingest_pd: DataFrame = read_csv(filepath_or_buffer=file_location, sep=",", header=None, names=names_list, nrows=num_rows)
    else:
        raise SyntaxError
    return ingest_pd


def ingest_file(file: UploadFile, table: str, num_rows: Optional[int] = None) -> tuple[DataFrame, str]:
    # write file to tmp storage
    try:
        if file.filename is not None:
            file_loc: str = join(OUTPUT_LOCATION, f"{str(uuid4())}-{file.filename}")
        else:
            raise UploadException
        contents: str = file.file.read().decode("utf-8")
        icl(contents)
        with open(file=file_loc, mode="w") as f:
            f.write(contents)
    except Exception as e:
        print("An error ocurred during uploading")
        icl(e)
        raise RuntimeError
    # get table column names
    names: list[str] = _get_table_header(table_name=table)
    # convert to dataframe
    ingest_pd: DataFrame = _ingest_csv_data(file_location=file_loc, names_list=names, num_rows=num_rows)
    # check data integrity
    if not len(names) == len(ingest_pd.columns):
        raise AttributeError
    icl(ingest_pd)
    return (ingest_pd, file_loc)


def main() -> None:
    return None


if __name__ == "__main__":
    main()
else:
    pass
