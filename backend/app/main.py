from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.core.lifespan import lifespan
from app.core.health import HealthService
from app.core.settings import settings
from app.core.dependencies import get_db, get_health_service
from app.api.v1.ai import router as ai_router
from app.shared.exceptions.handlers import register_exception_handlers
from app.shared.middleware.request_logging import RequestLoggingMiddleware
from app.shared.middleware.request_id import RequestIDMiddleware
#from app.modules.destination.api import router as destination_router
from app.api.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,

    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    register_exception_handlers(app)
    app.include_router(api_router)
    app.include_router(
        ai_router,
        prefix="/api/v1",
    )

    @app.get("/")
    async def root():
        return {
            "application": settings.app_name,
            "version": settings.app_version,
        }

    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "application": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "ai": {
                "enabled": settings.AI_ENABLED,
                "provider": settings.AI_PROVIDER,
            },
            "storage": {
                "provider": "local",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @app.get("/ready")
    async def ready(
        db: Session = Depends(get_db),
        health_service: HealthService = Depends(get_health_service),
    ):
        database_status = health_service.check_database(db)

        return {
            "status": "not_ready" if database_status == "down" else "ready",
            "application": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "checks": {
                "database": database_status,
                "ai": health_service.check_ai(),
                "storage": health_service.check_storage(),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    return app


app = create_app()