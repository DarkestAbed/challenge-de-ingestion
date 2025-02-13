# app/backend/app.py

from fastapi import FastAPI

from app.backend.lib.database import heartbeat


app = FastAPI(
    debug=True,
    title="Legacy data ingestion platform",
    summary="",
    description="",
    version="0.1.0",
    on_startup=None,
    on_shutdown=None,
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
    return {}
