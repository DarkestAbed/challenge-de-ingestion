# app/backend/asserts/tables_ddl.py

from typing import Any

from app.backend.lib.database import HiredEmployees, Jobs, Departments


TABLES: list[str] = ["hiredemployees", "departments", "jobs"]
TABLES_OBJ: dict[str, Any] = {
    "hiredemployees": HiredEmployees,
    "jobs": Jobs,
    "departments": Departments,
}
