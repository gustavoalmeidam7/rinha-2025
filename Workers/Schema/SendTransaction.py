from pydantic import BaseModel, field_serializer, field_validator

from datetime import datetime, timezone

import uuid

class SendTransaction(BaseModel):
    correlationId: uuid.UUID
    amount: float
    requestedAt: datetime = datetime.now(timezone.utc)

    @field_validator("amount", mode="before")
    def validade_total_amount(cls, value):
        return round(float(value), 2)

    @field_serializer('requestedAt')
    def serialize_requestedAt(self, requestedAt: datetime) -> str:
        return requestedAt.isoformat()
    
    @field_serializer('correlationId')
    def serialize_correlationId(self, correlationId: uuid.UUID) -> str:
        return str(correlationId)
    
    @field_serializer('amount')
    def serialize_amount(self, amount: float) -> str:
        return str(round(amount, 2))
        
