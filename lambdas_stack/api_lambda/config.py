from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    VERSION: str = None


@lru_cache
def get_config():
    config = Config()
    return config
