from fastapi import Request
from fastapi.responses import JSONResponse


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


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if isinstance(exc, FinTrackException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )