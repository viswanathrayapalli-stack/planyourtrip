from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.booking.repository import BookingRepository
from app.modules.checklist.repository import ChecklistRepository
from app.modules.expense.repository import ExpenseRepository
from app.modules.itinerary.repository import ItineraryRepository
from app.modules.note.repository import NoteRepository
from app.modules.trip.repository import TripRepository
from app.modules.dashboard.schemas import (
    DashboardResponse,
    DashboardStatistics,
    TripSummary,
)
from app.shared.exceptions.exceptions import ResourceNotFoundException


class DashboardService:

    def __init__(
        self,
        trip_repository: TripRepository,
        booking_repository: BookingRepository,
        expense_repository: ExpenseRepository,
        checklist_repository: ChecklistRepository,
        note_repository: NoteRepository,
        itinerary_repository: ItineraryRepository,
    ):
        self.trip_repository = trip_repository
        self.booking_repository = booking_repository
        self.expense_repository = expense_repository
        self.checklist_repository = checklist_repository
        self.note_repository = note_repository
        self.itinerary_repository = itinerary_repository

    def get_dashboard(
        self,
        db: Session,
        trip_id: int,
    ) -> DashboardResponse:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        bookings = self.booking_repository.get_by_trip_id(db, trip_id)
        expenses = self.expense_repository.get_by_trip_id(db, trip_id)
        checklists = self.checklist_repository.get_by_trip_id(db, trip_id)
        notes = self.note_repository.get_by_trip_id(db, trip_id)
        itineraries = self.itinerary_repository.get_by_trip_id(db, trip_id)

        total_bookings = len(bookings)
        total_expenses = len(expenses)
        total_expense_amount = sum((expense.amount for expense in expenses), Decimal(0))
        completed_checklists = sum(1 for checklist in checklists if checklist.is_completed)
        pending_checklists = sum(1 for checklist in checklists if not checklist.is_completed)
        total_notes = len(notes)
        itinerary_days = len(itineraries)

        return DashboardResponse(
            trip=TripSummary(
                id=trip.id,
                title=trip.title,
                description=trip.description,
            ),
            statistics=DashboardStatistics(
                total_bookings=total_bookings,
                total_expenses=total_expenses,
                total_expense_amount=total_expense_amount,
                completed_checklists=completed_checklists,
                pending_checklists=pending_checklists,
                total_notes=total_notes,
                itinerary_days=itinerary_days,
            ),
        )
