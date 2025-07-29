from pydantic import BaseModel, field_validator

class SummaryItem(BaseModel):
    totalRequests: int
    totalAmount: float

    @field_validator("totalAmount", mode="before")
    def validade_total_amount(cls, value):
        return round(value, 2)

class PaymentsSummary(BaseModel):
    default: SummaryItem
    fallback: SummaryItem
