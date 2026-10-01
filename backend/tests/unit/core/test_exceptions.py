from unittest.mock import MagicMock

import pytest
from fastapi import Request

from app.core.exceptions import (
    AccountNotFoundException,
    global_exception_handler,
)


@pytest.mark.anyio
async def test_global_exception_handler_returns_internal_server_error():
    request = MagicMock(spec=Request)
    exception = RuntimeError("Unexpected error")

    response = await global_exception_handler(
        request,
        exception,
    )

    assert response.status_code == 500
    assert response.body == b'{"detail":"Internal server error"}'


def test_account_not_found_exception_contains_expected_message():
    exception = AccountNotFoundException()

    assert str(exception) == "Account not found"


@pytest.mark.anyio
async def test_global_exception_handler_returns_account_not_found():
    request = MagicMock(spec=Request)
    exception = AccountNotFoundException()

    response = await global_exception_handler(
        request,
        exception,
    )

    assert response.status_code == 404
    assert response.body == b'{"detail":"Account not found"}'

