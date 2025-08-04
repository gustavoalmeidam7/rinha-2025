from redis.asyncio import Redis
import redis.asyncio as aioredis

from Utils.Env import env

redis = Redis(
    host="redis",
    decode_responses=True
)
