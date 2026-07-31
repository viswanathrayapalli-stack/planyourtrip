from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class Place(AuditMixin, Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    place_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    destination_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("destinations.id"),
        nullable=False,
    )

    destination = relationship(
        "Destination",
        back_populates="places",
    )
