# tests/functional/test_reports.py

from pandas import DataFrame

from app.backend.reports.employees_by_quarter import get_employees_by_quarter
from app.backend.reports.hirings_by_department import get_mean_hires, get_departments_over_mean


YEAR: int = 2021


def test_report_query():
    result = get_employees_by_quarter()
    assert isinstance(result, DataFrame)


def test_mean_hires():
    result = get_mean_hires(year=YEAR)
    assert isinstance(result, DataFrame)


def test_departments_over_hires():
    result = get_departments_over_mean()
    assert isinstance(result, DataFrame)
