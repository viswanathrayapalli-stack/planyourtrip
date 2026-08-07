from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TripSummary(BaseModel):
    id: int
    title: str
    description: str | None = None


class DashboardStatistics(BaseModel):
    total_bookings: int
    total_expenses: int
    total_expense_amount: Decimal
    completed_checklists: int
    pending_checklists: int
    total_notes: int
    itinerary_days: int


class DashboardResponse(BaseModel):
    trip: TripSummary
    statistics: DashboardStatistics

    model_config = ConfigDict(from_attributes=True)
