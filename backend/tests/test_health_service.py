from types import SimpleNamespace

from sqlalchemy.exc import SQLAlchemyError

from app.core.health import HealthService


class FakeDB:
    def __init__(self) -> None:
        self.statements: list[object] = []

    def execute(self, statement: object) -> None:
        self.statements.append(statement)


def test_check_database_returns_up_when_database_is_available() -> None:
    fake_db = FakeDB()
    settings = SimpleNamespace(AI_ENABLED=True, AI_PROVIDER="mock")
    health_service = HealthService(settings)

    result = health_service.check_database(fake_db)

    assert result == "up"
    assert len(fake_db.statements) == 1


def test_check_database_returns_down_when_database_check_raises_sqlalchemy_error() -> None:
    class FailingDB:
        def execute(self, statement: object) -> None:
            raise SQLAlchemyError("database unavailable")

    settings = SimpleNamespace(AI_ENABLED=True, AI_PROVIDER="mock")
    health_service = HealthService(settings)

    result = health_service.check_database(FailingDB())

    assert result == "down"


def test_check_ai_returns_configured_ai_settings() -> None:
    settings = SimpleNamespace(AI_ENABLED=True, AI_PROVIDER="mock")
    health_service = HealthService(settings)

    assert health_service.check_ai() == {
        "enabled": True,
        "provider": "mock",
    }


def test_check_storage_returns_local_provider() -> None:
    settings = SimpleNamespace(AI_ENABLED=False, AI_PROVIDER="openai")
    health_service = HealthService(settings)

    assert health_service.check_storage() == {
        "provider": "local",
    }
