import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.base import create_app
from extensions.sqlalchemy import drop_db, engine, get_db_session, sync_db


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def app():
    await sync_db()

    _app = create_app()
    try:
        yield _app
    finally:
        # 每次跑完测试清除数据库
        await drop_db()


@pytest.fixture
async def session(app: FastAPI) -> AsyncSession:
    async with engine.begin() as connection:
        async_session_local = async_sessionmaker(
            bind=connection,
            autoflush=False,
            future=True,
            autocommit=False,
            expire_on_commit=False
        )
        async_session = async_session_local()
        # Overwrite the current database so that every time the test is run, the transaction is rollback
        app.dependency_overrides[get_db_session] = lambda: async_session
        yield async_session
        await async_session.close()

        await connection.rollback()


@pytest_asyncio.fixture
async def client(app: FastAPI, session: AsyncSession):
    async with AsyncClient(
        app=app, base_url='http://testserver'
    ) as async_client:
        yield async_client
