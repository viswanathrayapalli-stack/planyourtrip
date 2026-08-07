from datetime import time
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class Itinerary(AuditMixin, Base):
    __tablename__ = "itineraries"
    __table_args__ = (
        UniqueConstraint("trip_id", "day_number", name="uq_itinerary_trip_day"),
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

    day_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    trip = relationship(
        "Trip",
        back_populates="itineraries",
    )

    activities = relationship(
        "ItineraryActivity",
        back_populates="itinerary",
        cascade="all, delete-orphan",
    )


class ItineraryActivity(AuditMixin, Base):
    __tablename__ = "itinerary_activities"
    __table_args__ = (
        UniqueConstraint("itinerary_id", "activity_order", name="uq_itinerary_activity_order"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    itinerary_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("itineraries.id"),
        nullable=False,
    )

    place_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("places.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    activity_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    end_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    estimated_duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    transport_mode: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    estimated_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    itinerary = relationship(
        "Itinerary",
        back_populates="activities",
    )

    place = relationship(
        "Place",
        back_populates="itinerary_activities",
    )
