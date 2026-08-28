from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="REST API for personal finance and transaction management.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(
    api_v1_router,
    prefix=settings.API_V1_PREFIX,
)