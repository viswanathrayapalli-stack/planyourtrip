from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.modules.favorite.models import Favorite
from app.shared.query_builder import QueryBuilder
from app.shared.repositories.base_repository import BaseRepository


class FavoriteRepository(BaseRepository[Favorite]):

    def __init__(self):
        super().__init__(Favorite)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Favorite]:
        stmt = (
            QueryBuilder(select(Favorite))
            .where(Favorite.trip_id == trip_id)
            .options(joinedload(Favorite.place))
            .order_by(Favorite.created_at.desc())
            .build()
        )
        return list(db.scalars(stmt).all())

    def get_by_trip_and_place(
        self,
        db: Session,
        trip_id: int,
        place_id: int,
    ) -> Favorite | None:
        stmt = (
            select(Favorite)
            .where(
                Favorite.trip_id == trip_id,
                Favorite.place_id == place_id,
            )
        )
        return db.scalar(stmt)


favorite_repository = FavoriteRepository()
