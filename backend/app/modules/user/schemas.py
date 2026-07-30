from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.shared.schemas import TimestampResponse


class UserBase(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=100,
    )


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100,
    )

    is_active: bool | None = None


class UserResponse(UserBase, TimestampResponse):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)