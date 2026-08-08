from sqlalchemy.orm import Session

from app.modules.booking.constants import BOOKING_NOT_FOUND
from app.modules.booking.models import Booking
from app.modules.booking.repository import BookingRepository
from app.modules.booking.schemas import BookingCreate, BookingResponse, BookingUpdate
from app.shared.authorization import AuthorizationService
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException
from app.shared.pagination import PageResponse, PaginationParams


class BookingService:

    def __init__(
        self,
        repository: BookingRepository,
        trip_repository: TripRepository,
        authorization_service: AuthorizationService,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.authorization_service = authorization_service

    def get_all(
        self,
        db: Session,
    ) -> list[Booking]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        booking_id: int,
        user_id: int,
    ) -> Booking:
        booking = self.repository.get_by_id(db, booking_id)

        if booking is None:
            raise ResourceNotFoundException(BOOKING_NOT_FOUND)

        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=booking.trip_id,
            current_user_id=user_id,
        )

        return booking

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> list[Booking]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        return self.repository.get_by_trip_id(db, trip_id)

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[BookingResponse]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        page = self.repository.get_by_trip_id_paginated(
            db=db,
            trip_id=trip_id,
            pagination=pagination,
        )

        return PageResponse(
            items=[BookingResponse.model_validate(booking) for booking in page.items],
            total=page.total,
            page=page.page,
            page_size=page.page_size,
            total_pages=page.total_pages,
        )

    def create(
        self,
        db: Session,
        request: BookingCreate,
        user_id: int,
    ) -> Booking:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=request.trip_id,
            current_user_id=user_id,
        )

        booking = Booking(**request.model_dump())

        return self.repository.create(db, booking)

    def update(
        self,
        db: Session,
        booking_id: int,
        request: BookingUpdate,
        user_id: int,
    ) -> Booking:
        booking = self.get_by_id(db, booking_id, user_id)
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(booking, key, value)

        return self.repository.update(db, booking)

    def delete(
        self,
        db: Session,
        booking_id: int,
        user_id: int,
    ) -> None:
        booking = self.get_by_id(db, booking_id, user_id)
        self.repository.delete(db, booking)
