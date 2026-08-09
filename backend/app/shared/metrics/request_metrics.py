import threading
from typing import Any


class RequestMetrics:
    """Track lightweight in-process request statistics."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._total_requests = 0
        self._requests_by_method: dict[str, int] = {}
        self._requests_by_status: dict[str, int] = {}
        self._requests_by_path: dict[str, int] = {}
        self._total_duration_ms = 0.0

    def record_completed_request(
        self,
        method: str,
        path: str,
        status_code: int | str,
        duration_ms: float,
    ) -> None:
        with self._lock:
            self._total_requests += 1
            self._requests_by_method[method] = self._requests_by_method.get(method, 0) + 1
            status_key = str(status_code)
            self._requests_by_status[status_key] = self._requests_by_status.get(status_key, 0) + 1
            self._requests_by_path[path] = self._requests_by_path.get(path, 0) + 1
            self._total_duration_ms += duration_ms

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            total_requests = self._total_requests
            average_duration_ms = (
                self._total_duration_ms / total_requests if total_requests else 0.0
            )

            return {
                "total_requests": total_requests,
                "requests_by_method": dict(self._requests_by_method),
                "requests_by_status": dict(self._requests_by_status),
                "requests_by_path": dict(self._requests_by_path),
                "total_duration_ms": self._total_duration_ms,
                "average_duration_ms": average_duration_ms,
            }


request_metrics = RequestMetrics()
