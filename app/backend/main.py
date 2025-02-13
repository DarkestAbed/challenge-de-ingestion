# app/backend/app.py

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.backend.assets.config import DB_TYPE
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


@app.post("/tables/{tablename}")
async def _(tablename: str):
    return {"status": "wip"}
