from fastapi import APIRouter

from app.api.v1.transactions import router as transactions_router
from app.api.v1.accounts import router as accounts_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router


router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "fintrack-api",
        "version": "v1",
    }


router.include_router(auth_router)
router.include_router(users_router)
router.include_router(accounts_router)
router.include_router(transactions_router)