from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.modules.trip_share.models import TripShare
from app.shared.query_builder import QueryBuilder
from app.shared.repositories.base_repository import BaseRepository


class TripShareRepository(BaseRepository[TripShare]):

    def __init__(self):
        super().__init__(TripShare)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[TripShare]:
        stmt = (
            QueryBuilder(select(TripShare))
            .where(TripShare.trip_id == trip_id)
            .options(joinedload(TripShare.user))
            .order_by(TripShare.created_at.asc())
            .build()
        )
        return list(db.scalars(stmt).all())

    def get_by_trip_and_user(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> TripShare | None:
        stmt = (
            select(TripShare)
            .where(
                TripShare.trip_id == trip_id,
                TripShare.user_id == user_id,
            )
        )
        return db.scalar(stmt)


trip_share_repository = TripShareRepository()
