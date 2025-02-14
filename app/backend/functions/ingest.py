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


def ingest_file(file: UploadFile, table: str, num_rows: Optional[int] = None) -> DataFrame:
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
    if num_rows is None:
        ingest_pd: DataFrame = read_csv(filepath_or_buffer=file_loc, sep=",", header=None, names=names)
    elif isinstance(num_rows, int) and num_rows > 0 and num_rows <= 1000:
        ingest_pd: DataFrame = read_csv(filepath_or_buffer=file_loc, sep=",", header=None, names=names, nrows=num_rows)
    else:
        raise SyntaxError
    # check data integrity
    if not len(names) == len(ingest_pd.columns):
        raise AttributeError
    icl(ingest_pd)
    return ingest_pd


def main() -> None:
    return None


if __name__ == "__main__":
    main()
else:
    pass
