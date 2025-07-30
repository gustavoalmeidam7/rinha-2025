from redis.asyncio import Redis
import redis.asyncio as aioredis

from Payments.Utils.Env import env

redis = Redis(
    host=env.get("redis_host"),
    decode_responses=True
)
