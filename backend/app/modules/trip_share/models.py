from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class TripShare(AuditMixin, Base):
    __tablename__ = "trip_shares"
    __table_args__ = (
        UniqueConstraint("trip_id", "user_id", name="uq_trip_share_trip_user"),
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

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    permission: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    trip = relationship(
        "Trip",
        back_populates="trip_shares",
    )

    user = relationship(
        "User",
        back_populates="shared_trips",
    )
