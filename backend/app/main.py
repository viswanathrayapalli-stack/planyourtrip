from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.settings import settings
from app.shared.exceptions.handlers import register_exception_handlers
from app.modules.destination.api import router as destination_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,

    )

    register_exception_handlers(app)
    app.include_router(destination_router)

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
            "environment": settings.environment,
        }

    return app


app = create_app()