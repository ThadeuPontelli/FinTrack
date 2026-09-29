from sqlalchemy.orm import Session

from app.models.account import Account
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate


class AccountService:

    @staticmethod
    def create_account(
        db: Session,
        account_data: AccountCreate,
        user_id: int,
    ) -> Account:
        account = Account(
            name=account_data.name,
            account_type=account_data.account_type,
            balance=0,
            user_id=user_id,
        )

        return AccountRepository.create(
            db,
            account,
        )

    @staticmethod
    def get_account(
        db: Session,
        account_id: int,
        user_id: int,
    ) -> Account | None:
        return AccountRepository.get_by_id(
            db,
            account_id,
            user_id,
        )

    @staticmethod
    def get_user_accounts(
        db: Session,
        user_id: int,
    ) -> list[Account]:
        return AccountRepository.get_all_by_user(
            db,
            user_id,
        )
