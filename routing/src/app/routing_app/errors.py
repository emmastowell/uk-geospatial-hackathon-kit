"""Errors returned to API callers in Valhalla's own JSON error shape."""

from typing import Any


class RoutingError(Exception):
    """A request Valhalla, or the App in front of it, could not serve."""

    def __init__(self, status_code: int, error_code: int, message: str, status: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.status = status

    def body(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "error": self.message,
            "status_code": self.status_code,
            "status": self.status,
        }
