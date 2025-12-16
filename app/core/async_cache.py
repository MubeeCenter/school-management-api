import redis.asyncio as redis
import json

redis_client = redis.from_url(
    "redis://localhost:6379",
    decode_responses=True
)

async def get_cache(key: str):
    data = await redis_client.get(key)
    return json.loads(data) if data else None

async def set_cache(key: str, value, ttl: int = 300):
    await redis_client.set(key, json.dumps(value), ex=ttl)

async def delete_cache(key: str):
    await redis_client.delete(key)
