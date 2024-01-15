from fastapi import APIRouter
from sqlalchemy import and_, select

from apps.user.exceptions import (
    AccountOrPasswordWrong,
    UserAlreadyExist,
    UserNotFound,
)
from apps.user.schemas import LoginOut, UserIn, UserOut
from extensions.fastapi.api import get, post
from extensions.fastapi.context import AppContext, DependsOnContext
from extensions.jwt import CurrentUser, DependsOnUser, generate_token
from models import User
from utils.config import get_config

router = APIRouter(prefix='/v1/users')
config = get_config()


@post(router, '/sign_up', response_model=UserOut)
async def sign_up(user_in: UserIn, context: AppContext = DependsOnContext):
    user = await context.sa_session.scalar(
        select(User).where(and_(User.username == user_in.username))
    )
    if user:
        raise UserAlreadyExist

    user = await User.new(username=user_in.username, password=user_in.password)
    context.sa_session.add(user)
    await context.sa_session.commit()
    return user


@post(router, '/login', response_model=LoginOut)
async def login(user_in: UserIn, context: AppContext = DependsOnContext):
    user = await context.sa_session.scalar(
        select(User).where(and_(User.username == user_in.username))
    )
    if not user:
        raise UserNotFound

    if not await user.verify_password(user_in.password):
        raise AccountOrPasswordWrong

    token = await generate_token(UserOut.from_orm(user).dict())
    await context.redis.set(
        f'{config.SERVICE_NAME}:user:token:{user.id}', token,
        config.EXPIRED_SECONDS
    )

    return {'token': token, 'user': user}


@get(router, '/', response_model=UserOut)
async def get_user_detail(current_user: CurrentUser = DependsOnUser):
    return current_user
