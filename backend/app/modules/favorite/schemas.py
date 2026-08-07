from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteCreate(BaseModel):
    trip_id: int
    place_id: int


class FavoriteResponse(BaseModel):
    id: int
    trip_id: int
    place_id: int
    place_name: str
    city: str
    country: str
    place_type: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
