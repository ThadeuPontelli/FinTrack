from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionType
from app.services.transaction_service import TransactionService


def test_create_income_transaction_updates_account_balance():
    db = MagicMock()

    account = Account(
        id=1,
        name="Conta Teste",
        account_type="checking",
        balance=Decimal("1000.00"),
        user_id=1,
    )

    db.get.return_value = account

    transaction_data = TransactionCreate(
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME,
    )

    with patch(
        "app.services.transaction_service.TransactionRepository.create"
    ):
        transaction = TransactionService.create_transaction(
            db=db,
            transaction_data=transaction_data,
            account_id=1,
        )

    assert account.balance == Decimal("1500.00")
    assert transaction.description == "Salário"
    assert transaction.amount == Decimal("500.00")
    assert transaction.transaction_type == "income"
    assert transaction.account_id == 1

    db.commit.assert_called_once()

def test_create_expense_transaction_updates_account_balance():
    db = MagicMock()

    account = Account(
        id=1,
        name="Conta Teste",
        account_type="checking",
        balance=Decimal("1000.00"),
        user_id=1,
    )

    db.get.return_value = account

    transaction_data = TransactionCreate(
        description="Supermercado",
        amount=Decimal("250.00"),
        transaction_type=TransactionType.EXPENSE,
    )

    with patch(
        "app.services.transaction_service.TransactionRepository.create"
    ):
        transaction = TransactionService.create_transaction(
            db=db,
            transaction_data=transaction_data,
            account_id=1,
        )

    assert account.balance == Decimal("750.00")
    assert transaction.description == "Supermercado"
    assert transaction.amount == Decimal("250.00")
    assert transaction.transaction_type == "expense"
    assert transaction.account_id == 1

    db.commit.assert_called_once()

def test_delete_income_transaction_reverts_account_balance():
    db = MagicMock()

    account = Account(
        id=1,
        name="Conta Teste",
        account_type="checking",
        balance=Decimal("1500.00"),
        user_id=1,
    )

    transaction = Transaction(
        id=1,
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME.value,
        account_id=1,
    )

    db.get.return_value = account

    with patch(
        "app.services.transaction_service.TransactionRepository.get_by_id",
        return_value=transaction,
    ), patch(
        "app.services.transaction_service.TransactionRepository.delete"
    ):
        deleted = TransactionService.delete_transaction(
            db=db,
            transaction_id=1,
            account_id=1,
        )

    assert deleted is True
    assert account.balance == Decimal("1000.00")

    db.commit.assert_called_once()

def test_delete_expense_transaction_reverts_account_balance():
    db = MagicMock()

    account = Account(
        id=1,
        name="Conta Teste",
        account_type="checking",
        balance=Decimal("750.00"),
        user_id=1,
    )

    transaction = Transaction(
        id=1,
        description="Supermercado",
        amount=Decimal("250.00"),
        transaction_type=TransactionType.EXPENSE.value,
        account_id=1,
    )

    db.get.return_value = account

    with patch(
        "app.services.transaction_service.TransactionRepository.get_by_id",
        return_value=transaction,
    ), patch(
        "app.services.transaction_service.TransactionRepository.delete"
    ):
        deleted = TransactionService.delete_transaction(
            db=db,
            transaction_id=1,
            account_id=1,
        )

    assert deleted is True
    assert account.balance == Decimal("1000.00")

    db.commit.assert_called_once()

def test_delete_transaction_returns_false_when_transaction_does_not_exist():
    db = MagicMock()

    with patch(
        "app.services.transaction_service.TransactionRepository.get_by_id",
        return_value=None,
    ):
        deleted = TransactionService.delete_transaction(
            db=db,
            transaction_id=999,
            account_id=1,
        )

    assert deleted is False
    db.commit.assert_not_called()

def test_delete_transaction_returns_false_when_account_does_not_exist():
    db = MagicMock()
    db.get.return_value = None

    transaction = Transaction(
        id=1,
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME.value,
        account_id=1,
    )

    with patch(
        "app.services.transaction_service.TransactionRepository.get_by_id",
        return_value=transaction,
    ):
        deleted = TransactionService.delete_transaction(
            db=db,
            transaction_id=1,
            account_id=1,
        )

    assert deleted is False
    db.commit.assert_not_called()

def test_create_transaction_rolls_back_when_account_does_not_exist():
    db = MagicMock()
    db.get.return_value = None

    transaction_data = TransactionCreate(
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME,
    )

    with patch(
        "app.services.transaction_service.TransactionRepository.create"
    ):
        try:
            TransactionService.create_transaction(
                db=db,
                transaction_data=transaction_data,
                account_id=999,
            )
        except ValueError as error:
            assert str(error) == "Account not found"
        else:
            raise AssertionError("Expected ValueError")

    db.rollback.assert_called_once()
    db.commit.assert_not_called()

def test_create_transaction_rolls_back_when_repository_fails():
    db = MagicMock()

    transaction_data = TransactionCreate(
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME,
    )

    repository_error = RuntimeError("Database error")

    with patch(
        "app.services.transaction_service.TransactionRepository.create",
        side_effect=repository_error,
    ):
        try:
            TransactionService.create_transaction(
                db=db,
                transaction_data=transaction_data,
                account_id=1,
            )
        except RuntimeError as error:
            assert error is repository_error
        else:
            raise AssertionError("Expected RuntimeError")

    db.rollback.assert_called_once()
    db.commit.assert_not_called()

def test_get_transaction_returns_transaction():
    db = MagicMock()

    transaction = Transaction(
        id=1,
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME.value,
        account_id=1,
    )

    with patch(
        "app.services.transaction_service.TransactionRepository.get_by_id",
        return_value=transaction,
    ) as repository_get:
        result = TransactionService.get_transaction(
            db=db,
            transaction_id=1,
            account_id=1,
        )

    assert result is transaction

    repository_get.assert_called_once_with(
        db,
        1,
        1,
    )

def test_get_account_transactions_returns_transactions():
    db = MagicMock()

    transactions = [
        Transaction(
            id=1,
            description="Salário",
            amount=Decimal("5000.00"),
            transaction_type=TransactionType.INCOME.value,
            account_id=1,
        ),
        Transaction(
            id=2,
            description="Supermercado",
            amount=Decimal("250.00"),
            transaction_type=TransactionType.EXPENSE.value,
            account_id=1,
        ),
    ]

    with patch(
        "app.services.transaction_service.TransactionRepository.get_all_by_account",
        return_value=transactions,
    ) as repository_get:
        result = TransactionService.get_account_transactions(
            db=db,
            account_id=1,
        )

    assert result == transactions

    repository_get.assert_called_once_with(
        db,
        1,
    )

def test_delete_transaction_rolls_back_when_repository_delete_fails():
    db = MagicMock()

    account = Account(
        id=1,
        name="Conta Teste",
        account_type="checking",
        balance=Decimal("1500.00"),
        user_id=1,
    )

    transaction = Transaction(
        id=1,
        description="Salário",
        amount=Decimal("500.00"),
        transaction_type=TransactionType.INCOME.value,
        account_id=1,
    )

    db.get.return_value = account

    repository_error = RuntimeError("Database error")

    with patch(
        "app.services.transaction_service.TransactionRepository.get_by_id",
        return_value=transaction,
    ), patch(
        "app.services.transaction_service.TransactionRepository.delete",
        side_effect=repository_error,
    ):
        try:
            TransactionService.delete_transaction(
                db=db,
                transaction_id=1,
                account_id=1,
            )
        except RuntimeError as error:
            assert error is repository_error
        else:
            raise AssertionError("Expected RuntimeError")

    db.rollback.assert_called_once()
    db.commit.assert_not_called()