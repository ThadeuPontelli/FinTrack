import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class FinTrackException(Exception):
    """Base exception for expected FinTrack application errors."""

    status_code = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class AccountNotFoundException(FinTrackException):
    """Raised when an account cannot be found."""

    status_code = 404

    def __init__(self):
        super().__init__("Account not found")

class CategoryNotFoundException(FinTrackException):
    """Raised when a category cannot be found."""

    status_code = 404

    def __init__(self):
        super().__init__("Category not found")

async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if isinstance(exc, FinTrackException):
        logger.warning(
            "Application exception: %s",
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
        )

    logger.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )