from pathlib import Path

from pydantic import BaseSettings
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename: str = 'logs/celery.log'
    log_level: str = 'INFO'

    broker_url: str
    single_beat_identifier: str
    single_beat_redis_server: str

    class Config:
        env_file = ENV_FILE


@lru_cache()
def get_settings():
    return Settings()

