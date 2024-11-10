from typing import Annotated

import pydantic.dataclasses
from aioredis.client import Redis
from fastapi.params import Depends
from pydantic import ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from extensions.aioredis import yield_async_redis_session
from extensions.sqlmodel import yield_async_db_session


@pydantic.dataclasses.dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class AppContext:
    request: Request | None
    response: Response | None
    sa_session: AsyncSession | None
    redis: Redis | None


async def get_app_ctx(
    request: Request,
    response: Response,
    sa_session: AsyncSession = Depends(yield_async_db_session),
    redis: Redis = Depends(yield_async_redis_session)
) -> AppContext:
    return AppContext(
        request=request, response=response, sa_session=sa_session, redis=redis
    )


DependsOnContext = Annotated[AppContext, Depends(get_app_ctx)]
