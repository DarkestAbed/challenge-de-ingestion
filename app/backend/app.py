# app/backend/app.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def _():
    return {"message": "Hello, world!"}


@app.get("/heartbeat")
async def _():
    return {"HEARTBEAT": 1}


@app.get("/tables/")
async def _():
    return {}
