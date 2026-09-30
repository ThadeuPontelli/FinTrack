from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account


class AccountRepository:

    @staticmethod
    def create(
        db: Session,
        account: Account,
    ) -> Account:
        db.add(account)
        db.flush()
        db.refresh(account)

        return account

    @staticmethod
    def get_by_id(
        db: Session,
        account_id: int,
        user_id: int,
    ) -> Account | None:
        statement = select(Account).where(
            Account.id == account_id,
            Account.user_id == user_id,
        )

        return db.scalar(statement)

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int,
    ) -> list[Account]:
        statement = (
            select(Account)
            .where(Account.user_id == user_id)
            .order_by(Account.id)
        )

        return list(db.scalars(statement).all())
