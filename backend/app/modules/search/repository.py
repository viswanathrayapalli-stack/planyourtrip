from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.trip.models import Trip
from app.shared.repositories.base_repository import BaseRepository


class TripSearchRepository(BaseRepository[Trip]):

    def __init__(self):
        super().__init__(Trip)

    def search_by_title(
        self,
        db: Session,
        keyword: str,
    ) -> list[Trip]:
        stmt = (
            select(Trip)
            .where(Trip.title.ilike(f"%{keyword}%"))
            .order_by(Trip.created_at.desc())
        )

        return list(db.scalars(stmt).all())


trip_search_repository = TripSearchRepository()