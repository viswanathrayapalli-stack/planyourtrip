from pydantic import BaseModel, ConfigDict


class DestinationCreate(BaseModel):
    name: str
    country: str
    description: str | None = None

class DestinationUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    description: str | None = None
    is_active: bool | None = None

class DestinationResponse(BaseModel):
    id: int
    name: str
    country: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)