from sqlmodel import SQLModel


async def sync_db(async_engine):
    """同步数据库,用于单元测试初始化数据库
    """
    from extensions.sqlalchemy_utils import create_database, database_exists

    if not await database_exists(async_engine.url):
        # 创建测试数据库
        await create_database(async_engine.url)

    async with async_engine.begin() as session:
        await session.run_sync(SQLModel.metadata.create_all)


async def drop_db(async_engine):
    """清除数据库表,用于运行完单元测试后执行
    """
    async with async_engine.begin() as session:
        await session.run_sync(SQLModel.metadata.drop_all)
