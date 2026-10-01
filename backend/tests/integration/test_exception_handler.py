from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.core.exceptions import AccountNotFoundException
from app.main import app


def test_global_exception_handler_returns_500():
    test_router = APIRouter()

    @test_router.get("/test-exception")
    def raise_exception():
        raise RuntimeError("Unexpected error")

    app.include_router(test_router)

    app.debug = False

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get("/test-exception")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal server error",
    }


def test_global_exception_handler_returns_account_not_found():
    test_router = APIRouter()

    @test_router.get("/test-account-not-found")
    def raise_account_not_found():
        raise AccountNotFoundException()

    app.include_router(test_router)

    app.debug = False

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get("/test-account-not-found")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account not found",
    }

