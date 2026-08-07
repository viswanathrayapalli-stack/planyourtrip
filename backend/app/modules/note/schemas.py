from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str
    note_type: str | None = None
    trip_id: int


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    note_type: str | None = None


class NoteResponse(BaseModel):
    id: int
    trip_id: int
    title: str
    content: str
    note_type: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
