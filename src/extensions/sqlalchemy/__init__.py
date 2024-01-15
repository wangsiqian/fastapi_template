from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta, registry
from sqlalchemy.pool import QueuePool

from utils.config import get_config

config = get_config()
engine = create_async_engine(
    config.aio_db_url(),
    echo=config.DB_ENABLE_ECHO,
    pool_size=config.DB_POOL_SIZE,
    max_overflow=config.DB_POOL_OVERFLOW,
    poolclass=QueuePool
)
async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    """数据库模型基类
    """
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata
    __init = mapper_registry.constructor


async def get_db_session() -> AsyncSession:
    """项目中获取数据库 session
    """
    async_session = async_scoped_session(async_session_factory, current_task)
    try:
        yield async_session()
    finally:
        await async_session.close()


async def sync_db():
    """同步数据库,用于单元测试初始化数据库
    """
    from extensions.sqlalchemy_utils import create_database, database_exists

    if not await database_exists(engine.url):
        # 创建测试数据库
        await create_database(engine.url)

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)


async def drop_db():
    """清除数据库表,用于运行完单元测试后执行
    """
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
