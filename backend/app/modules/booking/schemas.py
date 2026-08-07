from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    booking_type: str
    provider: str | None = None
    booking_reference: str | None = None
    status: str = "PLANNED"
    booking_date: date | None = None
    travel_date: date | None = None
    amount: Decimal | None = None
    currency: str = "INR"
    notes: str | None = None
    trip_id: int


class BookingUpdate(BaseModel):
    booking_type: str | None = None
    provider: str | None = None
    booking_reference: str | None = None
    status: str | None = None
    booking_date: date | None = None
    travel_date: date | None = None
    amount: Decimal | None = None
    currency: str | None = None
    notes: str | None = None
    


class BookingResponse(BaseModel):
    id: int
    trip_id: int
    booking_type: str
    provider: str | None = None
    booking_reference: str | None = None
    status: str
    booking_date: date | None = None
    travel_date: date | None = None
    amount: Decimal | None = None
    currency: str
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
