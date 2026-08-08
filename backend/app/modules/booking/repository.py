from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.booking.models import Booking
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories.base_repository import BaseRepository


class BookingRepository(BaseRepository[Booking]):

    def __init__(self):
        super().__init__(Booking)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.trip_id == trip_id)
            .order_by(Booking.travel_date.asc())
        )
        return list(db.scalars(stmt).all())

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.trip_id == trip_id)
            .order_by(Booking.travel_date.asc())
        )
        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


booking_repository = BookingRepository()
