from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ExpenseCreate(BaseModel):
    expense_category: str
    title: str
    description: str | None = None
    amount: Decimal
    currency: str = "INR"
    expense_date: date
    payment_method: str | None = None
    notes: str | None = None
    trip_id: int


class ExpenseUpdate(BaseModel):
    expense_category: str | None = None
    title: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    currency: str | None = None
    expense_date: date | None = None
    payment_method: str | None = None
    notes: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    trip_id: int
    expense_category: str
    title: str
    description: str | None = None
    amount: Decimal
    currency: str
    expense_date: date
    payment_method: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
