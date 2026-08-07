from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base
from app.shared.models import AuditMixin


class Trip(AuditMixin, Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    itineraries = relationship(
        "Itinerary",
        back_populates="trip",
    )

    bookings = relationship(
        "Booking",
        back_populates="trip",
    )
    
    expenses = relationship(
        "Expense",
        back_populates="trip",
    )

    checklists = relationship(
        "Checklist",
        back_populates="trip",
    )

    notes = relationship(
        "Note",
        back_populates="trip",
    )

    favorites = relationship(
        "Favorite",
        back_populates="trip",
        cascade="all, delete-orphan",
    )