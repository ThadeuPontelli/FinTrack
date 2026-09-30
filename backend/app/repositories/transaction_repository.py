from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(
        db: Session,
        transaction: Transaction,
    ) -> Transaction:
        db.add(transaction)
        db.flush()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_by_id(
        db: Session,
        transaction_id: int,
        account_id: int,
    ) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.account_id == account_id,
        )

        return db.scalar(statement)

    @staticmethod
    def get_all_by_account(
        db: Session,
        account_id: int,
    ) -> list[Transaction]:
        statement = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.id)
        )

        return list(db.scalars(statement).all())
    
    @staticmethod
    def delete(
        db: Session,
        transaction: Transaction,
    ) -> None:
        db.delete(transaction)
        db.flush()