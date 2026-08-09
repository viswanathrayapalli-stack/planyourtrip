from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.exceptions.exceptions import (
    AppException,
    AuthenticationException,
)
from app.shared.logging.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        headers = {}

        # RFC 6750 - Required for Bearer authentication failures
        if isinstance(exc, AuthenticationException):
            headers["WWW-Authenticate"] = "Bearer"

        request_id = getattr(getattr(request, "state", None), "request_id", None)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
                "request_id": request_id,
            },
            headers=headers,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):
        request_id = getattr(getattr(request, "state", None), "request_id", None)
        logger.exception(
            "Unhandled exception occurred request_id=%s",
            request_id,
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error.",
                "data": None,
                "request_id": request_id,
            },
        )