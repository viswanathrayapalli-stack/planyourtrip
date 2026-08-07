from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AttachmentCreate(BaseModel):
    trip_id: int
    file_name: str
    original_file_name: str
    file_type: str
    file_size: int
    file_path: str
    category: str


class AttachmentResponse(BaseModel):
    id: int
    trip_id: int
    file_name: str
    original_file_name: str
    file_type: str
    file_size: int
    file_path: str
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
