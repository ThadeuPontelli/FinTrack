from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCreate(BaseModel):
    description: str = Field(
        min_length=1,
        max_length=255,
    )

    amount: Decimal = Field(
        gt=0,
    )

    transaction_type: TransactionType

    category_id: int | None = None


class TransactionResponse(BaseModel):
    id: int
    description: str
    amount: Decimal
    transaction_type: TransactionType
    account_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

    category_id: int | None