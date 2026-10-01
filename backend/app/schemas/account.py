from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CASH = "cash"

class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    account_type: AccountType


class AccountResponse(BaseModel):
    id: int
    name: str
    account_type: str
    balance: Decimal
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
