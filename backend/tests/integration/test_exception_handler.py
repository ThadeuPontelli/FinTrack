from fastapi import APIRouter
from fastapi.testclient import TestClient

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
