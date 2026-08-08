from fastapi import Query
from pydantic import BaseModel


class StatusFilterParams(BaseModel):
    status: str | None = Query(
        default=None,
        description="Filter by status",
    )