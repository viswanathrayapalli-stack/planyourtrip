from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base
from app.shared.models import AuditMixin



class Destination(AuditMixin,Base):
    __tablename__ = "destinations"

    #id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    