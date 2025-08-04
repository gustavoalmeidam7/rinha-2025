from pydantic import BaseModel, field_validator

class SummaryBeam(BaseModel):
    totalRequests: int = 0
    totalAmount: float = 0.00
    
    @field_validator('totalAmount', mode="before")
    def validator_totalAmount(cls, totalAmount):
        return round(totalAmount, 2)

class SummarySchema(BaseModel):
    default: SummaryBeam = SummaryBeam()
    fallback: SummaryBeam = SummaryBeam()
