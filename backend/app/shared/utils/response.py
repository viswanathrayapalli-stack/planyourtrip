from typing import Any

from app.shared.schemas.api_response import ApiResponse


def success_response(
    data: Any = None,
    message: str = "Success",
) -> ApiResponse:
    return ApiResponse(
        success=True,
        message=message,
        data=data,
    )


def error_response(
    message: str,
) -> ApiResponse:
    return ApiResponse(
        success=False,
        message=message,
        data=None,
    )