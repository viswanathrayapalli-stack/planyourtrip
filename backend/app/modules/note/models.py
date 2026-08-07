from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class Note(AuditMixin, Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    trip_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("trips.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    note_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    trip = relationship(
        "Trip",
        back_populates="notes",
    )
