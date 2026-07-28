from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PlanYourTrip API"
    app_version: str = "0.1.0"

    environment: str = "development"
    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    database_url: str = (
        "postgresql://postgres:password@localhost:5432/planyourtrip"
    )

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()