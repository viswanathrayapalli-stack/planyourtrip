from sqlalchemy.orm import Session

from app.modules.booking.repository import BookingRepository
from app.modules.checklist.repository import ChecklistRepository
from app.modules.expense.repository import ExpenseRepository
from app.modules.itinerary.repository import ItineraryRepository
from app.modules.note.repository import NoteRepository
from app.modules.timeline.schemas import TimelineEvent, TimelineResponse
from app.modules.trip.repository import TripRepository
from app.shared.authorization import AuthorizationService


class TimelineService:

    def __init__(
        self,
        trip_repository: TripRepository,
        booking_repository: BookingRepository,
        itinerary_repository: ItineraryRepository,
        expense_repository: ExpenseRepository,
        checklist_repository: ChecklistRepository,
        note_repository: NoteRepository,
        authorization_service: AuthorizationService,
    ):
        self.trip_repository = trip_repository
        self.booking_repository = booking_repository
        self.itinerary_repository = itinerary_repository
        self.expense_repository = expense_repository
        self.checklist_repository = checklist_repository
        self.note_repository = note_repository
        self.authorization_service = authorization_service

    def get_timeline(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> TimelineResponse:
        trip = self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        bookings = self.booking_repository.get_by_trip_id(db, trip_id)
        itineraries = self.itinerary_repository.get_by_trip_id(db, trip_id)
        expenses = self.expense_repository.get_by_trip_id(db, trip_id)
        checklists = self.checklist_repository.get_by_trip_id(db, trip_id)
        notes = self.note_repository.get_by_trip_id(db, trip_id)

        events: list[TimelineEvent] = []

        for booking in bookings:
            events.append(
                TimelineEvent(
                    date=booking.created_at.date(),
                    type="Booking",
                    title=booking.booking_reference,
                    description=booking.booking_type,
                )
            )

        for itinerary in itineraries:
            events.append(
                TimelineEvent(
                    date=itinerary.created_at.date(),
                    type="Itinerary",
                    title=itinerary.title,
                    description=itinerary.notes,
                )
            )

        for expense in expenses:
            events.append(
                TimelineEvent(
                    date=expense.expense_date,
                    type="Expense",
                    title=expense.title,
                    description=expense.expense_category,
                )
            )

        for checklist in checklists:
            event_date = (
                checklist.due_date
                if checklist.due_date is not None
                else checklist.created_at.date()
            )
            events.append(
                TimelineEvent(
                    date=event_date,
                    type="Checklist",
                    title=checklist.title,
                    description=checklist.category,
                )
            )

        for note in notes:
            events.append(
                TimelineEvent(
                    date=note.created_at.date(),
                    type="Note",
                    title=note.title,
                    description=note.note_type,
                )
            )

        events.sort(key=lambda event: event.date)

        return TimelineResponse(
            trip_id=trip.id,
            events=events,
        )
