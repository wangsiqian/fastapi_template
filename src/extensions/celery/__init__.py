import logging
from concurrent.futures import ThreadPoolExecutor

from celery import Celery
from fastapi import FastAPI

from utils.config import get_config

config = get_config()
celery_app = Celery(
    'fastapi_template',
    broker=config.CELERY_BROKER,
    backend=config.CELERY_BACKEND
)


class CeleryManagement:
    logger = logging.getLogger('CeleryManagement')

    def __init__(self, app: FastAPI):
        self.app = app
        self.thread_pool = ThreadPoolExecutor(max_workers=1)

    @classmethod
    def start_celery_worker(cls):
        if not config.CELERY_ENABLED:
            return

        worker_instance = celery_app.Worker()
        worker_instance.start()
        cls.logger.info('Celery startup complete')

    async def startup(self):
        self.thread_pool.submit(self.start_celery_worker)

    def shutdown(self):
        celery_app.control.shutdown()
        self.thread_pool.shutdown()

    def init(self):
        self.app.add_event_handler('startup', self.startup)
        self.app.add_event_handler('shutdown', self.shutdown)
