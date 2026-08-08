from fastapi import Query
from pydantic import BaseModel


class TripFilterParams(BaseModel):
    destination: str | None = Query(default=None)
    status: str | None = Query(default=None)
