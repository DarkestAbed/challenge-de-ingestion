# app/backend/app.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, HTTPException
from os.path import join
from typing import Any

from app.backend.assets.config import DB_TYPE, OUTPUT_LOCATION, icl
from app.backend.lib.database import Database

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


@app.get("/")
async def _():
    return {"message": "Hello, world!"}


@app.get("/heartbeat")
async def _():
    response: bool = db.heartbeat()
    if response:
        return {"HEARTBEAT": 1}
    else:
        return {"HEARTBEAT": 0}


@app.get("/tables")
async def _():
    response: list[str] = db.get_tables()
    return {"tables": response}


@app.get("/tables/{tablename}")
async def _(tablename: str):
    response: bool = db.check_table(table_name=tablename)
    return {"table": tablename, "exists": response}


@app.post("/tables/{tablename}")
async def _(tablename: str, file: UploadFile):
    icl(file.content_type, file.filename, file.headers, file.size)
    check_table: bool = db.check_table(table_name=tablename)
    if not check_table:
        return HTTPException(status_code=404, detail="Table does not exists")
    try:
        if file.filename is not None:
            file_loc: str = join(OUTPUT_LOCATION, file.filename)
        else:
            return HTTPException(status_code=402, detail="Empty file uploaded")
        contents: Any = file.file.read().decode("utf-8")
        icl(contents)
        with open(file=file_loc, mode="w") as f:
            f.write(contents)
    except Exception as e:
        ...

    return {"status": "wip", "requested_table": tablename}
