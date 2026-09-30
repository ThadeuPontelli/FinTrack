from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService


router = APIRouter(
    prefix="/accounts/{account_id}/transactions",
    tags=["Transactions"],
)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    account_id: int,
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = AccountRepository.get_by_id(
        db=db,
        account_id=account_id,
        user_id=current_user.id,
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return TransactionService.create_transaction(
        db=db,
        transaction_data=transaction_data,
        account_id=account_id,
    )

@router.get(
    "",
    response_model=list[TransactionResponse],
)
def get_transactions(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = AccountRepository.get_by_id(
        db=db,
        account_id=account_id,
        user_id=current_user.id,
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    return TransactionService.get_account_transactions(
        db=db,
        account_id=account_id,
    )

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    account_id: int,
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = AccountRepository.get_by_id(
        db=db,
        account_id=account_id,
        user_id=current_user.id,
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    transaction = TransactionService.get_transaction(
        db=db,
        transaction_id=transaction_id,
        account_id=account_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    return transaction

@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transaction(
    account_id: int,
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = AccountRepository.get_by_id(
        db=db,
        account_id=account_id,
        user_id=current_user.id,
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    deleted = TransactionService.delete_transaction(
        db=db,
        transaction_id=transaction_id,
        account_id=account_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )