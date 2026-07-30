from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.shared.exceptions.exceptions import (
    AppException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)

def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )
    @app.exception_handler(ResourceAlreadyExistsException)
    async def already_exists_handler(
        request: Request,
        exc: ResourceAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )

    @app.exception_handler(ResourceNotFoundException)
    async def not_found_handler(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )