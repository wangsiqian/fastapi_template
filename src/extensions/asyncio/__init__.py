import asyncio
from functools import partial

from extensions.threadpool import (
    THREAD_POOL_BLOCK_TASK,
    ThreadPoolExecutorManager,
)


async def async_run(func, *args, **kwargs):
    loop = asyncio.get_event_loop()

    partial_sync_func = partial(func, *args, **kwargs)
    executor = ThreadPoolExecutorManager.get_thread_pool(THREAD_POOL_BLOCK_TASK)

    return await loop.run_in_executor(executor, partial_sync_func)
