# app/backend/app.py

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.backend.lib.database import heartbeat, setup_init


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_init()
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


@app.get("/")
async def _():
    return {"message": "Hello, world!"}


@app.get("/heartbeat")
async def _():
    response: bool = heartbeat()
    if response:
        return {"HEARTBEAT": 1}
    else:
        return {"HEARTBEAT": 0}


@app.get("/tables/")
async def _():
    return {"status": "wip"}
