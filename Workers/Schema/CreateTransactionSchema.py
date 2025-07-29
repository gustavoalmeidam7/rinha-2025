from pydantic import BaseModel, field_validator

import uuid

class CreateTransaction(BaseModel):
    correlationId: uuid.UUID
    amount: float

    @field_validator("amount", mode="before")
    def validade_amount(cls, value) -> float:
        return round(value, 2)
