from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse
from app.services.account_service import AccountService


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.create_account(
        db=db,
        account_data=account_data,
        user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[AccountResponse],
)
def get_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.get_user_accounts(
        db=db,
        user_id=current_user.id,
    )
