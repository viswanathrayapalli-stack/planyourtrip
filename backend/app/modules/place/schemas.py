from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PlaceCreate(BaseModel):
    name: str
    city: str
    state: Optional[str] = None
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    place_type: Optional[str] = None
    destination_id: int


class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    place_type: Optional[str] = None
    destination_id: Optional[int] = None


class PlaceResponse(BaseModel):
    id: int
    name: str
    city: str
    state: Optional[str] = None
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    place_type: Optional[str] = None
    destination_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
