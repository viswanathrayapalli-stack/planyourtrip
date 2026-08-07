from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.checklist.models import Checklist
from app.shared.repositories.base_repository import BaseRepository


class ChecklistRepository(BaseRepository[Checklist]):

    def __init__(self):
        super().__init__(Checklist)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Checklist]:
        stmt = (
            select(Checklist)
            .where(Checklist.trip_id == trip_id)
            .order_by(Checklist.due_date.asc())
        )

        return list(db.scalars(stmt).all())


checklist_repository = ChecklistRepository()
