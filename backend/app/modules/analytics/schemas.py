from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CategoryExpense(BaseModel):
    category: str
    amount: Decimal


class BudgetSummaryResponse(BaseModel):
    trip_id: int
    currency: str
    total_expenses: int
    total_amount: Decimal
    categories: list[CategoryExpense]

    model_config = ConfigDict(from_attributes=True)

class ChecklistProgress(BaseModel):
    completed: int
    pending: int
    completion_percentage: float

class BookingProgress(BaseModel):
    total: int

class ItineraryProgress(BaseModel):
    days: int

class NoteProgress(BaseModel):
    total: int

class TripProgressResponse(BaseModel):
    trip_id: int
    checklists: ChecklistProgress
    bookings: BookingProgress
    itinerary: ItineraryProgress
    notes: NoteProgress

    model_config = ConfigDict(from_attributes=True)
