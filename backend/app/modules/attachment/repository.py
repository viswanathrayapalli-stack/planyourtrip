from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.attachment.models import Attachment
from app.shared.repositories.base_repository import BaseRepository


class AttachmentRepository(BaseRepository[Attachment]):

    def __init__(self):
        super().__init__(Attachment)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Attachment]:
        stmt = (
            select(Attachment)
            .where(Attachment.trip_id == trip_id)
            .order_by(Attachment.created_at.desc())
        )
        return list(db.scalars(stmt).all())


attachment_repository = AttachmentRepository()
