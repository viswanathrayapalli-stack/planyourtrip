from sqlalchemy.orm import Session

from app.modules.booking.constants import BOOKING_NOT_FOUND
from app.modules.booking.models import Booking
from app.modules.booking.repository import BookingRepository
from app.modules.booking.schemas import BookingCreate, BookingUpdate
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException


class BookingService:

    def __init__(
        self,
        repository: BookingRepository,
        trip_repository: TripRepository,
    ):
        self.repository = repository
        self.trip_repository = trip_repository

    def get_all(
        self,
        db: Session,
    ) -> list[Booking]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        booking_id: int,
    ) -> Booking:
        booking = self.repository.get_by_id(db, booking_id)

        if booking is None:
            raise ResourceNotFoundException(BOOKING_NOT_FOUND)

        return booking

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Booking]:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        return self.repository.get_by_trip_id(db, trip_id)

    def create(
        self,
        db: Session,
        request: BookingCreate,
    ) -> Booking:
        trip = self.trip_repository.get_by_id(db, request.trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        booking = Booking(**request.model_dump())

        return self.repository.create(db, booking)

    def update(
        self,
        db: Session,
        booking_id: int,
        request: BookingUpdate,
    ) -> Booking:
        booking = self.get_by_id(db, booking_id)
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(booking, key, value)

        return self.repository.update(db, booking)

    def delete(
        self,
        db: Session,
        booking_id: int,
    ) -> None:
        booking = self.get_by_id(db, booking_id)
        self.repository.delete(db, booking)
