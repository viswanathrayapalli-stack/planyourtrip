from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = Query(default=1, ge=1)
    page_size: int = Query(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
