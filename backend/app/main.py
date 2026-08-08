from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.core.settings import settings
from app.api.v1.ai import router as ai_router
from app.shared.exceptions.handlers import register_exception_handlers
#from app.modules.destination.api import router as destination_router
from app.api.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,

    )

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
            "environment": settings.environment,
        }

    return app


app = create_app()