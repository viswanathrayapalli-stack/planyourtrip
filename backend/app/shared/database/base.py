from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all SQLAlchemy models here so Alembic can discover them.
from app.modules.destination.models import Destination  # noqa: E402,F401