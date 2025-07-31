from typing import List
from pydantic import BaseModel, field_serializer, field_validator

from datetime import datetime, timezone

import uuid

class Transaction(BaseModel):
    correlationId: str
    amount: float
    requestedAt: datetime = datetime.now(timezone.utc)
    isFallback: bool = False

    @field_validator("amount", mode="before")
    def validade_total_amount(cls, value):
        return round(float(value), 2)

    @field_serializer('requestedAt')
    def serialize_requestedAt(self, requestedAt: datetime) -> str:
        return requestedAt.isoformat()
    
    @field_serializer('amount')
    def serialize_amount(self, amount: float) -> str:
        return str(round(amount, 2))
    
class PaymentsSummary(BaseModel):
    Transactions: List[Transaction] = []
