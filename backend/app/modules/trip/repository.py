from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.trip.models import Trip
from app.shared.repositories import BaseRepository


class TripRepository(BaseRepository[Trip]):

    def __init__(self):
        super().__init__(Trip)

    def get_by_id_and_user(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> Trip | None:
        stmt = select(Trip).where(
            Trip.id == trip_id,
            Trip.user_id == user_id,
        )
        return db.scalar(stmt)

    def get_all_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Trip]:
        stmt = select(Trip).where(Trip.user_id == user_id)
        return list(db.scalars(stmt).all())


trip_repository = TripRepository()