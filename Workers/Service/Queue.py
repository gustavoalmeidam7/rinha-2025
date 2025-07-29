from Workers.DB import redis

from Workers.Schema.SendTransaction import SendTransaction
from Workers.Schema.HealthStatus import HealthStatuses

import json

def insert_health(health: HealthStatuses):
    redis.lpush("health", health.model_dump_json())

async def pop_transaction() -> SendTransaction | None:
    transaction = await redis.rpop("transactions") # type: ignore
    if transaction is None:
        return None
    
    transaction = json.loads(transaction) # type: ignore
    transaction = SendTransaction.model_validate(transaction)
    return transaction

async def insert_transaction(transaction: SendTransaction):
    await redis.lpush("transactions", transaction.model_dump_json()) # type: ignore
