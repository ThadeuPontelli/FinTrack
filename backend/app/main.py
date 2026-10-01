from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.exceptions import global_exception_handler
from app.core.logging import configure_logging


configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="REST API for personal finance and transaction management.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)

app.include_router(
    api_v1_router,
    prefix=settings.API_V1_PREFIX,
)