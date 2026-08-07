from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ChecklistCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    is_completed: bool = False
    due_date: date | None = None
    trip_id: int


class ChecklistUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    is_completed: bool | None = None
    due_date: date | None = None


class ChecklistResponse(BaseModel):
    id: int
    trip_id: int
    title: str
    description: str | None = None
    category: str | None = None
    is_completed: bool
    due_date: date | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
