from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.destination.models import Destination
from app.shared.repositories import BaseRepository


class DestinationRepository(BaseRepository[Destination]):

    def __init__(self):
        super().__init__(Destination)

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> Destination | None:
        stmt = select(Destination).where(Destination.name == name)
        return db.scalar(stmt)


destination_repository = DestinationRepository()