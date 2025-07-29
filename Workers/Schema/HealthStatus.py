from pydantic import BaseModel

class HealthStatus(BaseModel):
    isFailing: bool = True
    onTimeout: bool = False
    minResponseTime: int = 9999

class HealthStatuses(BaseModel):
    Default: HealthStatus = HealthStatus()
    Fallback: HealthStatus = HealthStatus()
