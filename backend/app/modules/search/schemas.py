from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TripSearchResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
