from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.settings import Settings


class HealthService:
    """Reusable service for application readiness checks."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def check_database(self, db: Session) -> str:
        """Run a lightweight database check and return status."""
        try:
            db.execute(text("SELECT 1"))
            return "up"
        except SQLAlchemyError:
            return "down"

    def check_ai(self) -> dict[str, bool | str]:
        """Return AI readiness configuration status."""
        return {
            "enabled": self.settings.AI_ENABLED,
            "provider": self.settings.AI_PROVIDER,
        }

    def check_storage(self) -> dict[str, str]:
        """Return storage provider readiness status."""
        return {
            "provider": "local",
        }