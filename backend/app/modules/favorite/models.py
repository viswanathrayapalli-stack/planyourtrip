from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class Favorite(AuditMixin, Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("trip_id", "place_id", name="uq_favorite_trip_place"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    trip_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("trips.id"),
        nullable=False,
    )

    place_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("places.id"),
        nullable=False,
    )

    trip = relationship(
        "Trip",
        back_populates="favorites",
    )

    place = relationship(
        "Place",
        back_populates="favorites",
    )
