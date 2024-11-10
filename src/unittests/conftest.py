import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from apps.base import create_app
from extensions.sqlmodel import yield_async_db_session
from unittests.utils import drop_db, sync_db
from utils.config import get_config

config = get_config()
async_engine = create_async_engine(
    config.DB_URL.replace(config.DB_DATABASE, f'{config.DB_DATABASE}_test'),
    echo=config.DB_ENABLE_ECHO,
    pool_size=config.DB_POOL_SIZE,
    max_overflow=config.DB_POOL_OVERFLOW,
    poolclass=AsyncAdaptedQueuePool
)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def app():
    await sync_db(async_engine)

    _app = create_app()
    try:
        yield _app
    finally:
        # 每次跑完测试清除数据库
        await drop_db(async_engine)


@pytest.fixture
async def session(app: FastAPI) -> AsyncSession:
    async with async_engine.begin() as connection:
        async_session = AsyncSession(
            bind=connection,
            autoflush=False,
            future=True,
            autocommit=False,
            expire_on_commit=False
        )
        # Overwrite the current database so that every time the test is run, the transaction is rollback
        app.dependency_overrides[yield_async_db_session] = lambda: async_session
        yield async_session
        await async_session.close()

        await connection.rollback()


@pytest_asyncio.fixture
async def client(app: FastAPI, session: AsyncSession):
    async with AsyncClient(
        app=app, base_url='http://testserver'
    ) as async_client:
        yield async_client
