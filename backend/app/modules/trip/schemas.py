from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import TimestampResponse


class TripCreate(BaseModel):
    title: str = Field(..., max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    is_active: bool = True


class TripUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    is_active: bool | None = None


class TripResponse(TimestampResponse):
    id: int
    title: str
    description: str | None
    is_active: bool