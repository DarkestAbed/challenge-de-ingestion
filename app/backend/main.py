# app/backend/app.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.concurrency import run_in_threadpool
from os import remove
from pandas import DataFrame
from traceback import print_exc
from typing import Any, Optional

from app.backend.assets.config import DB_TYPE, icl
from app.backend.functions.ingest import ingest_file
from app.backend.functions.load import load_data_into_db, dedupe_data_on_table
from app.backend.functions.automated_etl import etl, check_process
from app.backend.functions.lookup import get_data_snippet
from app.backend.lib.database import Database
from app.backend.lib.exceptions import DatabaseException, InsertException, UploadException

@asynccontextmanager
async def lifespan(app: FastAPI):
    _: Database = Database(db_type=DB_TYPE)        # type: ignore
    yield
    # cleanup database
    ...


app = FastAPI(
    debug=True,
    title="Legacy data ingestion platform",
    summary="",
    description="",
    version="0.1.0",
    lifespan=lifespan,      # type: ignore
)
db: Database = Database(db_type=DB_TYPE)        # type: ignore


@app.get(path="/")
async def _():
    return {"message": "Hello, world!"}


@app.get(path="/heartbeat")
async def _():
    response: bool = db.heartbeat()
    if response:
        return {"HEARTBEAT": 1}
    else:
        return {"HEARTBEAT": 0}


@app.get(path="/tables")
async def _():
    response: list[str] = db.get_tables()
    return {"tables": response}


@app.get(path="/tables/{tablename}")
async def _(tablename: str):
    response: bool = db.check_table(table_name=tablename)
    if response:
        snippet: Any = get_data_snippet(table_name=tablename)
    else:
        raise HTTPException(status_code=404, detail="Table not found")
    if snippet is False:
        return {"table": tablename, "details": "Table is empty"}
    else:
        return {"table": tablename, "data_preview": snippet}


@app.post(path="/tables/{tablename}")
async def _(tablename: str, file: UploadFile, rows_to_ingest: Optional[int] = None, dedupe: Optional[bool] = None):
    icl(file.content_type, file.filename, file.headers, file.size)
    check_table: bool = db.check_table(table_name=tablename)
    if not check_table:
        raise HTTPException(status_code=404, detail="Table does not exists")
    if not file.content_type == "text/csv":
        raise HTTPException(status_code=400, detail="Wrong type of file uploaded")
    # ingesting file into database
    ## reading in
    try:
        if rows_to_ingest is None:
            result: tuple[DataFrame, str] = await ingest_file(file=file, table=tablename)
        elif isinstance(rows_to_ingest, int):
            if rows_to_ingest < 0 or rows_to_ingest > 1000:
                raise ValueError
            result = await ingest_file(file=file, table=tablename, num_rows=rows_to_ingest)
        ingested_data: DataFrame = result[0]
        file_location: str = result[1]
        icl(file_location)
    except UploadException:
        raise HTTPException(status_code=400)
    except AttributeError:
        raise HTTPException(status_code=400, detail="Table not compatible with uploaded data")
    except RuntimeError:
        raise HTTPException(status_code=500)
    except SyntaxError:
        raise HTTPException(status_code=500)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unacceptable number of rows to read")
    except Exception as e:
        icl(e)
        raise HTTPException(status_code=500)
    ## writing to database
    try:
        affected_rows: int = load_data_into_db(table_pd=ingested_data, table_name=tablename)
        if dedupe:
            _ = dedupe_data_on_table(table_name=tablename)
    except DatabaseException:
        raise HTTPException(status_code=500)
    except InsertException:
        raise HTTPException(status_code=500)
    except Exception as e:
        icl(e)
        raise HTTPException(status_code=500)
    # cleaning up fs
    remove(path=file_location)
    # wrap up
    return {"status": "upload complete", "requested_table": tablename, "affected_rows": affected_rows}


@app.post(path="/etl/startProcess")
async def _(init: bool):
    if not init:
        raise HTTPException(status_code=400, detail="Process not started")
    try:
        icl("Start await")
        _ = await run_in_threadpool(etl)
        # yield {"process": "etl", "status": "init"}
        icl("End await")
    except RuntimeError:
        raise HTTPException(status_code=400, detail="A previous ETL is already running")
    except Exception as e:
        icl(e)
        print_exc()
        print("Something happened on the ETL process. Please review the logs and try again.")
        raise HTTPException(status_code=500)
    icl("Return status")
    return {"process": "etl", "status": "init"}


@app.get(path="/etl/check")
async def _():
    process_check: bool = check_process()
    if process_check:
        return {"process": "etl", "status": "done"}
    else:
        return {"process": "etl", "status": "running"}
