from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PlanYourTrip API"
    app_version: str = "0.1.0"

    # ==========================
    # AI Configuration
    # ==========================
    AI_ENABLED: bool = True
    AI_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.6-luna"
    OPENAI_BASE_URL: str | None = None

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@planyourtrip.com"
    SMTP_FROM_NAME: str = "PlanYourTrip"
    SMTP_USE_TLS: bool = False

    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS: list[str] = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    ]

    environment: str = "development"
    debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    database_url: str = (
        "postgresql+psycopg://postgres:password@localhost:5432/planyourtrip"
    )

    log_level: str = "INFO"

    # ==========================
    # JWT Authentication
    # ==========================
    secret_key: str = "change-this-to-a-secure-random-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()