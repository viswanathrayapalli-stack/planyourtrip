from datetime import time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import TimestampResponse


class ItineraryBase(BaseModel):
    day_number: int = Field(..., ge=1)
    title: str = Field(..., max_length=150)
    notes: str | None = Field(default=None, max_length=2000)


class ItineraryCreate(ItineraryBase):
    model_config = ConfigDict(extra="allow")


class ItineraryUpdate(BaseModel):
    day_number: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, max_length=150)
    notes: str | None = Field(default=None, max_length=2000)


class ItineraryResponse(ItineraryBase, TimestampResponse):
    id: int = Field(..., ge=1)
    trip_id: int = Field(..., ge=1)

    model_config = ConfigDict(from_attributes=True)


class ItineraryActivityBase(BaseModel):
    place_id: int | None = Field(default=None, ge=1)
    title: str = Field(..., max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    activity_order: int = Field(..., ge=1)
    start_time: time | None = None
    end_time: time | None = None
    estimated_duration_minutes: int | None = Field(default=None, ge=1)
    transport_mode: str | None = Field(default=None, max_length=50)
    estimated_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )
    notes: str | None = Field(default=None, max_length=2000)


class ItineraryActivityCreate(ItineraryActivityBase):
    model_config = ConfigDict(extra="allow")


class ItineraryActivityUpdate(BaseModel):
    place_id: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    activity_order: int | None = Field(default=None, ge=1)
    start_time: time | None = None
    end_time: time | None = None
    estimated_duration_minutes: int | None = Field(default=None, ge=1)
    transport_mode: str | None = Field(default=None, max_length=50)
    estimated_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )
    notes: str | None = Field(default=None, max_length=2000)


class ItineraryActivityResponse(ItineraryActivityBase, TimestampResponse):
    id: int = Field(..., ge=1)
    itinerary_id: int = Field(..., ge=1)

    model_config = ConfigDict(from_attributes=True)