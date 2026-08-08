from enum import Enum

from fastapi import Query
from pydantic import BaseModel


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortParams(BaseModel):
    sort_by: str | None = Query(default=None)
    sort_order: SortOrder = Query(default=SortOrder.DESC)
