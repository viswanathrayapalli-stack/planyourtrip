from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.exceptions.exceptions import (
    AppException,
    AuthenticationException,
)


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

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
            headers=headers,
        )