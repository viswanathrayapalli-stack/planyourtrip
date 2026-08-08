from collections import defaultdict
from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.analytics.schemas import (
    BudgetSummaryResponse,
    CategoryExpense,
    TripProgressResponse,
    ChecklistProgress,
    BookingProgress,
    ItineraryProgress,
    NoteProgress,
)
from app.modules.booking.repository import BookingRepository
from app.modules.checklist.repository import ChecklistRepository
from app.modules.expense.repository import ExpenseRepository
from app.modules.itinerary.repository import ItineraryRepository
from app.modules.note.repository import NoteRepository
from app.modules.trip.repository import TripRepository
from app.shared.authorization import AuthorizationService


class AnalyticsService:

    def __init__(
        self,
        trip_repository: TripRepository,
        expense_repository: ExpenseRepository,
        booking_repository: BookingRepository,
        checklist_repository: ChecklistRepository,
        note_repository: NoteRepository,
        itinerary_repository: ItineraryRepository,
        authorization_service: AuthorizationService,
    ):
        self.trip_repository = trip_repository
        self.expense_repository = expense_repository
        self.booking_repository = booking_repository
        self.checklist_repository = checklist_repository
        self.note_repository = note_repository
        self.itinerary_repository = itinerary_repository
        self.authorization_service = authorization_service

    def get_budget_summary(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> BudgetSummaryResponse:
        trip = self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        expenses = self.expense_repository.get_by_trip_id(db, trip_id)

        total_expenses = len(expenses)

        if total_expenses > 0:
            currency = expenses[0].currency
        else:
            currency = "INR"

        total_amount = sum((expense.amount for expense in expenses), Decimal(0))

        category_totals: dict[str, Decimal] = defaultdict(lambda: Decimal(0))

        for expense in expenses:
            category = expense.expense_category or ""
            category_totals[category] += expense.amount

        categories: list[CategoryExpense] = [
            CategoryExpense(category=cat, amount=amt)
            for cat, amt in category_totals.items()
        ]

        return BudgetSummaryResponse(
            trip_id=trip.id,
            currency=currency,
            total_expenses=total_expenses,
            total_amount=total_amount,
            categories=categories,
        )

    def get_trip_progress(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> TripProgressResponse:
        trip = self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        bookings = self.booking_repository.get_by_trip_id(db, trip_id)
        checklists = self.checklist_repository.get_by_trip_id(db, trip_id)
        notes = self.note_repository.get_by_trip_id(db, trip_id)
        itineraries = self.itinerary_repository.get_by_trip_id(db, trip_id)

        total_checklists = len(checklists)
        completed = sum(1 for c in checklists if getattr(c, "is_completed", False))
        pending = total_checklists - completed

        if total_checklists == 0:
            completion_percentage = 0.0
        else:
            completion_percentage = round((completed / total_checklists) * 100, 2)

        booking_progress = BookingProgress(total=len(bookings))
        checklist_progress = ChecklistProgress(
            completed=completed,
            pending=pending,
            completion_percentage=completion_percentage,
        )
        itinerary_progress = ItineraryProgress(days=len(itineraries))
        note_progress = NoteProgress(total=len(notes))

        return TripProgressResponse(
            trip_id=trip.id,
            checklists=checklist_progress,
            bookings=booking_progress,
            itinerary=itinerary_progress,
            notes=note_progress,
        )
