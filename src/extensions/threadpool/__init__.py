import logging
from concurrent.futures import ThreadPoolExecutor
from typing import cast

from fastapi import Depends, FastAPI

from utils.object import Singleton

THREAD_POOL_BLOCK_TASK = 'block_task'


class ThreadPoolExecutorManager(metaclass=Singleton):
    logger = logging.getLogger('ThreadPoolExecutorManager')
    thread_pool_executors = {}

    def __init__(self, app: FastAPI):
        self.app = app

    @classmethod
    def get_thread_pool(cls, thread_pool_name):
        return cls.thread_pool_executors.get(thread_pool_name)

    def add_thread_pool(
        self, thread_pool_name, max_workers=None, thread_name_prefix=''
    ):
        if not thread_name_prefix:
            thread_name_prefix = thread_pool_name

        thread_pool = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix=thread_name_prefix
        )
        self.thread_pool_executors[thread_pool_name] = thread_pool
        self.logger.info(f'add new thread pool: {thread_pool_name}')

    def shutdown(self):
        for name, thread_pool_executor in self.thread_pool_executors.items():
            thread_pool_executor.shutdown()
            self.logger.info(f'{name} shutdown.')

    def init(self):
        self.add_thread_pool(THREAD_POOL_BLOCK_TASK)
        self.app.add_event_handler('shutdown', self.shutdown)


def get_thread_pool_executor(thread_pool_name):
    """eg: thread_pool_executor: ThreadPoolExecutor = DependsOnBlockTaskTreadPool
    """

    def thread_pool_executor():
        return ThreadPoolExecutorManager.get_thread_pool(thread_pool_name)

    return thread_pool_executor


DependsOnBlockTaskTreadPool: ThreadPoolExecutor = cast(
    ThreadPoolExecutor,
    Depends(get_thread_pool_executor(THREAD_POOL_BLOCK_TASK))
)
