# app/backend/functions/ingest.py

import pandas as pd

from fastapi import UploadFile
from os.path import join
from typing import Any
from uuid import uuid4

from app.backend.assets.config import OUTPUT_LOCATION, icl
from app.backend.lib.exceptions import UploadException


def ingest_file(file: UploadFile) -> bool:
    try:
        if file.filename is not None:
            file_loc: str = join(OUTPUT_LOCATION, f"{str(uuid4())}-{file.filename}")
        else:
            raise UploadException
        contents: Any = file.file.read().decode("utf-8")
        icl(contents)
        with open(file=file_loc, mode="w") as f:
            f.write(contents)
    except Exception as e:
        print("An error ocurred during uploading")
        icl(e)
        raise UploadException
    
    return True


def main() -> None:
    return None
