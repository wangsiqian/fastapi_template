import importlib
import os
from functools import lru_cache

from extensions.base_configs import BaseConfig


def get_active_env():
    return os.getenv('STAGE')


@lru_cache(maxsize=1)
def get_config(config_name: str = None) -> BaseConfig:
    """
    if config name is none, get active profile from env
    """
    if not config_name:
        config_name = get_active_env()

    configs_module = importlib.import_module('configs')
    config_class = getattr(configs_module, config_name.capitalize())
    return config_class()
