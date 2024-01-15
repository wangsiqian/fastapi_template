from typing import cast

from aioredis.client import Redis
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from extensions.aioredis import get_redis
from extensions.sqlalchemy import get_db_session


class AppContext:

    def __init__(self):
        self.request: Request | None = None
        self.response: Response | None = None
        self.sa_session: AsyncSession | None = None
        self.redis: Redis | None = None


async def get_app_ctx(
    request: Request,
    response: Response,
    sa_session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis)
) -> AppContext:

    context = AppContext()
    context.request = request
    context.response = response
    context.sa_session = sa_session
    context.redis = redis
    return context


DependsOnContext: AppContext = cast(AppContext, Depends(get_app_ctx))
