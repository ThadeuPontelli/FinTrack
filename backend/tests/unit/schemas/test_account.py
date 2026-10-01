import pytest
from pydantic import ValidationError

from app.schemas.account import AccountCreate, AccountType


@pytest.mark.parametrize(
    "account_type",
    [
        AccountType.CHECKING,
        AccountType.SAVINGS,
        AccountType.CASH,
    ],
)
def test_account_create_accepts_valid_account_types(account_type):
    account = AccountCreate(
        name="Minha conta",
        account_type=account_type,
    )

    assert account.account_type == account_type


def test_account_create_rejects_invalid_account_type():
    with pytest.raises(ValidationError):
        AccountCreate(
            name="Minha conta",
            account_type="banana",
        )
        
def test_account_create_accepts_account_type_as_string():
    account = AccountCreate(
        name="Minha conta",
        account_type="checking",
    )

    assert account.account_type == AccountType.CHECKING