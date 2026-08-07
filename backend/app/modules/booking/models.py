from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class Booking(AuditMixin, Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    trip_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("trips.id"),
        nullable=False,
    )

    booking_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    provider: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    booking_reference: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="PLANNED",
        nullable=False,
    )

    booking_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    travel_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    trip = relationship(
        "Trip",
        back_populates="bookings",
    )
