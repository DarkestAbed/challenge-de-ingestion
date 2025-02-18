# app/backend/functions/automated_etl.py

from app.backend.assets.config import DB_TYPE, INPUT_LOCATION, OUTPUT_LOCATION


FILES_TO_LOAD: list[str] = ["jobs", "departments", ]


def extract():
    return None


def transform():
    return None


def load():
    return None


def etl():
    extract()
    transform()
    load()
    return None
