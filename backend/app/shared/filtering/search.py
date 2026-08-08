from fastapi import Query
from pydantic import BaseModel


class SearchParams(BaseModel):
    q: str | None = Query(
        default=None,
        description="Search keyword",
    )