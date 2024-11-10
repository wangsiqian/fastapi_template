from typing import Annotated, cast

import jwt
from aioredis import Redis
from fastapi import Depends, Header
from pydantic import BaseModel, ValidationError

from extensions.aioredis import yield_async_redis_session
from extensions.jwt.exceptions import (
    AlgorithmError,
    ApiSignatureExpired,
    JsonError,
    JwtTokenError,
)
from utils.config import get_config

config = get_config()


async def generate_token(payload):
    return jwt.encode(payload=payload, key=config.SECRET_KEY)


async def parse_token(token):
    try:
        payload = jwt.decode(
            token, key=config.SECRET_KEY, algorithms=config.SECRET_ALGORITHMS
        )
    except jwt.ExpiredSignatureError:
        raise ApiSignatureExpired
    except jwt.DecodeError:
        raise JsonError
    except jwt.InvalidAlgorithmError:
        raise AlgorithmError
    except jwt.InvalidTokenError:
        raise JwtTokenError

    return payload


class CurrentUser(BaseModel):
    id: int
    username: str


async def get_current_user(
    token: str = Header('token'),
    redis: Redis = Depends(yield_async_redis_session)
):
    if not token:
        raise ApiSignatureExpired

    payload = await parse_token(token)

    if 'id' in payload:
        try:
            current_user = CurrentUser.parse_obj(payload)
        except ValidationError:
            raise JwtTokenError

        cache_token = await redis.get(
            f'{config.SERVICE_NAME}:user:token:{current_user.id}'
        )
        if cache_token != token:
            raise ApiSignatureExpired

        return current_user

    raise ApiSignatureExpired


DependsOnUser = Annotated[CurrentUser, Depends(get_current_user)]
