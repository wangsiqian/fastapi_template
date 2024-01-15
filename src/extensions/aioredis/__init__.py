import aioredis
from aioredis.client import Redis

from utils.config import get_config

config = get_config()
redis = aioredis.from_url(config.REDIS_URL, decode_responses=True)


async def get_redis() -> Redis:
    client: Redis = await redis.client()
    try:
        yield client
    finally:
        await client.close()
