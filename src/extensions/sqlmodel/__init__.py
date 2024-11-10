from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel.ext.asyncio.session import AsyncSession

from utils.config import get_config

config = get_config()
async_engine = create_async_engine(
    config.DB_URL,
    echo=config.DB_ENABLE_ECHO,
    pool_size=config.DB_POOL_SIZE,
    max_overflow=config.DB_POOL_OVERFLOW,
    poolclass=AsyncAdaptedQueuePool
)


async def yield_async_db_session() -> AsyncSession:
    """项目中获取数据库 session
    """
    async with AsyncSession(
        bind=async_engine, expire_on_commit=False
    ) as session:
        yield session
