from datetime import date

from pydantic import BaseModel, ConfigDict


class TimelineEvent(BaseModel):
    date: date
    type: str
    title: str
    description: str | None = None


class TimelineResponse(BaseModel):
    trip_id: int
    events: list[TimelineEvent]

    model_config = ConfigDict(from_attributes=True)
