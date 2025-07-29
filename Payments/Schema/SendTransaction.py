from pydantic import BaseModel, field_serializer

from datetime import datetime, timezone

import uuid

class SendTransaction(BaseModel):
    correlationId: uuid.UUID
    amount: float
    requestedAt: datetime = datetime.now(timezone.utc)

    @field_serializer('requestedAt')
    def serialize_requestedAt(self, requestedAt: datetime) -> str:
        return requestedAt.isoformat()
    
    @field_serializer('amount')
    def serialize_amount(self, amount: float) -> str:
        return str(round(amount, 2))
