from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    # env settings
    STAGE = 'dev'

    # fastapi settings
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    DEBUG: bool = True
    SERVICE_NAME: str = 'fastapi_app'

    # pg settings
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'example'
    DB_HOST: str = '127.0.0.1'
    DB_POOL_SIZE: int = 20
    DB_POOL_OVERFLOW: int = 50
    DB_ENABLE_ECHO: bool = True

    # celery
    CELERY_ENABLED = True
    CELERY_BROKER = 'redis://127.0.0.1:6379/0'
    CELERY_BACKEND = 'redis://127.0.0.1:6379/0'

    # logger settings
    LOGGING_LEVEL: str = 'INFO'

    # aioredis settings
    # aioredis://[[username]:[password]]@localhost:6379/0
    REDIS_URL: str = 'redis://127.0.0.1:6379/0'

    # jwt settings
    SECRET_KEY: str = "aw(*@#Hha9s8dfy1h2342j349uh123872345365460912!x"
    SECRET_ALGORITHMS: list = ['HS256']
    EXPIRED_SECONDS: int = 3 * 24 * 60 * 60

    # pytest settings
    PYTEST_ARGS = ['-s', '-x', '-v', '-p', 'no:warnings', '--color=yes']

    def aio_db_url(self):
        """aio database url
        """
        return f'mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_DATABASE}'

    def db_url(self):
        """database url
        """
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_DATABASE}'

    def log_config(self):
        """日志配置
        """
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'root': {
                'level': self.LOGGING_LEVEL,
                'handlers': ['console']
            },
            'loggers': {
                # 默认配置, 通过logging.getLogger(__name__)拿到的logger配置
                '': {
                    'handlers': ['console',],
                    'level': self.LOGGING_LEVEL,
                    'propagate': True,
                },
                # 自定义, 通过logging.getLogger('fastapi')拿到的logger配置
                # propagate设置为False，关闭向上级logger传递，否则会出现重复输出
                self.SERVICE_NAME: {
                    'handlers': ['console',],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False,
                },
                'mysql': {
                    'handlers': ['console',],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False,
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'generic',
                    'stream': 'ext://sys.stdout'
                },
            },
            'formatters': {
                'generic': {
                    'format': (
                        '%(asctime)s [%(process)d] [%(levelname)s] '
                        '[%(name)s] %(message)s'
                    ),
                    'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
                    'class': 'logging.Formatter'
                }
            }
        }
