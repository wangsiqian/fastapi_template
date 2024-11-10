import aioredis
from aioredis.client import Redis

from utils.config import get_config

config = get_config()
redis = aioredis.from_url(config.REDIS_URL, decode_responses=True)


async def yield_async_redis_session() -> Redis:
    async with redis.client() as client:
        yield client
