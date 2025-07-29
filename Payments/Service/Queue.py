from Payments.DB import redis

from Payments.Schema.SendTransaction import SendTransaction

async def insert_transaction(transaction: SendTransaction):
    await redis.lpush("transactions", transaction.model_dump_json())
