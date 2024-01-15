"""
集群里的相关配置
"""
from extensions.base_configs import BaseConfig


class Development(BaseConfig):
    STAGE: str = 'dev'


class Docker(BaseConfig):
    STAGE = 'docker'

    DB_HOST = 'mysql'
    REDIS_URL = 'redis://redis:6379/0'


class Testing(BaseConfig):
    STAGE: str = 'test'

    # logger config
    LOGGING_LEVEL: str = 'DEBUG'

    # db config
    DB_DATABASE = 'example_test'
    DB_ENABLE_ECHO = False


class Production(BaseConfig):
    STAGE: str = 'prod'
    DEBUG: bool = False

    # logger config
    LOGGING_LEVEL: str = 'INFO'
