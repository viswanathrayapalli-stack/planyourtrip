from fastapi import Query
from pydantic import BaseModel


class TripFilterParams(BaseModel):
    is_active: bool | None = Query(default=None)
