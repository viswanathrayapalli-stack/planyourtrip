from datetime import date

from fastapi import Query
from pydantic import BaseModel


class DateRangeParams(BaseModel):
    start_date: date | None = Query(default=None)
    end_date: date | None = Query(default=None)