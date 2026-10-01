import logging

from sqlalchemy.orm import Session

from app.core.exceptions import AccountNotFoundException
from app.models.account import Account
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionType,
)

logger = logging.getLogger(__name__)

class TransactionService:

    @staticmethod
    def create_transaction(
        db: Session,
        transaction_data: TransactionCreate,
        account_id: int,
    ) -> Transaction:
        logger.info(
            "Creating transaction for account_id=%s, type=%s, amount=%s",
            account_id,
            transaction_data.transaction_type.value,
            transaction_data.amount,
        )

        try:
            transaction = Transaction(
                description=transaction_data.description,
                amount=transaction_data.amount,
                transaction_type=transaction_data.transaction_type.value,
                account_id=account_id,
            )
    
            TransactionRepository.create(
                db,
                transaction,
            )
    
            account = db.get(Account, account_id)
    
            if account is None:
                logger.warning(
                    "Account not found while creating transaction: account_id=%s",
                    account_id,
                )
                raise AccountNotFoundException()

            if transaction_data.transaction_type == TransactionType.INCOME:
                account.balance += transaction_data.amount
            else:
                account.balance -= transaction_data.amount
    
            db.commit()
            db.refresh(transaction)

            logger.info(
                "Transaction created successfully: transaction_id=%s, account_id=%s",
                transaction.id,
                account_id,
            )

            return transaction
    
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_transaction(
        db: Session,
        transaction_id: int,
        account_id: int,
    ) -> Transaction | None:
        return TransactionRepository.get_by_id(
            db,
            transaction_id,
            account_id,
        )

    @staticmethod
    def get_account_transactions(
        db: Session,
        account_id: int,
    ) -> list[Transaction]:
        return TransactionRepository.get_all_by_account(
            db,
            account_id,
        )

    @staticmethod
    def delete_transaction(
        db: Session,
        transaction_id: int,
        account_id: int,
    ) -> bool:
        try:
            transaction = TransactionRepository.get_by_id(
                db=db,
                transaction_id=transaction_id,
                account_id=account_id,
            )

            if transaction is None:
                return False

            account = db.get(Account, account_id)

            if account is None:
                return False

            if transaction.transaction_type == TransactionType.INCOME.value:
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount

            logger.info(
                "Deleting transaction: transaction_id=%s, account_id=%s",
                transaction_id,
                account_id,
            )

            TransactionRepository.delete(
                db=db,
                transaction=transaction,
            )

            db.commit()

            logger.info(
                "Transaction deleted successfully: transaction_id=%s, account_id=%s",
                transaction_id,
                account_id,
            )

            return True

        except Exception:
            db.rollback()
            raise
