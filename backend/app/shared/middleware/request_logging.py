import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.shared.logging import get_logger


logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log incoming requests and completed responses."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Record request/response metadata and request duration."""
        request_id = getattr(request.state, "request_id", "-")
        method = request.method
        path = request.url.path
        client_ip = request.client.host if request.client else "-"

        logger.info(
            "request.started request_id=%s method=%s path=%s client_ip=%s",
            request_id,
            method,
            path,
            client_ip,
        )

        start = time.perf_counter()
        response: Response | None = None

        try:
            response = await call_next(request)
            return response
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            status_code = response.status_code if response is not None else "ERROR"

            logger.info(
                "request.completed request_id=%s method=%s path=%s client_ip=%s status_code=%s duration_ms=%.2f",
                request_id,
                method,
                path,
                client_ip,
                status_code,
                duration_ms,
            )