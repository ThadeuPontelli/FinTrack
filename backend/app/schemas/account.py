from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    account_type: str = Field(min_length=1, max_length=50)


class AccountResponse(BaseModel):
    id: int
    name: str
    account_type: str
    balance: Decimal
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
