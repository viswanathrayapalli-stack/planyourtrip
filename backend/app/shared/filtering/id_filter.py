from fastapi import Query
from pydantic import BaseModel


class TripIdFilterParams(BaseModel):
    trip_id: int | None = Query(
        default=None,
        ge=1,
        description="Filter by Trip ID",
    )


class UserIdFilterParams(BaseModel):
    user_id: int | None = Query(
        default=None,
        ge=1,
        description="Filter by User ID",
    )