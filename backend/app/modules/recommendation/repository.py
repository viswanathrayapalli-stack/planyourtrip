from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.place.models import Place
from app.shared.repositories.base_repository import BaseRepository


class RecommendationRepository(BaseRepository[Place]):

    def __init__(self):
        super().__init__(Place)

    def get_by_destination_id(
        self,
        db: Session,
        destination_id: int,
    ) -> list[Place]:
        stmt = (
            select(Place)
            .where(Place.destination_id == destination_id)
            .order_by(Place.name.asc())
        )
        return list(db.scalars(stmt).all())


recommendation_repository = RecommendationRepository()
