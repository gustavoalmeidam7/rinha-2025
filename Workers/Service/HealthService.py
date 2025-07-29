from httpx import AsyncClient, TimeoutException
from fastapi import status
from enum import StrEnum
import asyncio

from Workers.Schema.HealthStatus import HealthStatuses
from Workers.Service.Queue import insert_health
from Workers.Utils.Env import env

healthStatuses = HealthStatuses()

class processors(StrEnum):
    Default = "http://localhost:8001"
    Fallback = "http://localhost:8002"

async def coroutine_get_health():
    executeHealtDelay = env.get("workers_health_delay")

    while True:
        await get_health()
        print("GET HEALTH FINISHED")

        await asyncio.sleep(executeHealtDelay)

async def get_health():
    try:
        async with AsyncClient() as client:
            response_default = await client.get(processors.Default + "/payments/service-health")
            response_fallback = await client.get(processors.Fallback + "/payments/service-health")

            if response_default.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                healthStatuses.Default.onTimeout = True
            
            if response_fallback.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                healthStatuses.Fallback.onTimeout = True

            jsonResponse_default = response_default.json()
            jsonResponse_fallback = response_fallback.json()
            
            healthStatuses.Default.isFailing = jsonResponse_default["failing"]
            healthStatuses.Default.minResponseTime = jsonResponse_default["minResponseTime"]

            healthStatuses.Fallback.isFailing = jsonResponse_fallback["failing"]
            healthStatuses.Fallback.minResponseTime = jsonResponse_fallback["minResponseTime"]
    except TimeoutException:
        healthStatuses.Default.isFailing = True
        healthStatuses.Default.minResponseTime = 999

        healthStatuses.Fallback.isFailing = True
        healthStatuses.Fallback.minResponseTime = 999

    # insert_health(healthStatuses)
