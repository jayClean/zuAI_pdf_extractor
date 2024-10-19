import json
from database import redis  # Import the Redis client

CACHE_TTL = 3600  # Time-to-live for cache entries in seconds (1 hour)

async def set_cache(key: str, value: dict):
    await redis.set(key, json.dumps(value), ex=CACHE_TTL)

async def get_cache(key: str):
    cached_data = await redis.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

async def invalidate_cache(key: str):
    await redis.delete(key)
