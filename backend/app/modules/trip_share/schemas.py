from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TripShareCreate(BaseModel):
    trip_id: int
    user_id: int
    permission: str


class TripShareResponse(BaseModel):
    id: int
    trip_id: int
    user_id: int
    user_name: str
    user_email: str
    permission: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
