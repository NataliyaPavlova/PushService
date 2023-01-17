from pathlib import Path

from pydantic import BaseSettings, Field
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename: str = 'logs/distributor.log'
    log_level: str = 'INFO'

    # onesignal_key: str
    # app_id: str
    # onesignal_url: str
    onesignal_key: str = Field(env='ONESIGNAL_KEY', default='Basic MWUyOWEwMTMtNTdhOC00NjQwLWI5M2YtZDVlMTY4ZDk0YTUw')
    onesignal_url: str = "https://onesignal.com/api/v1/notifications"
    app_id: str = "e77c7a41-2789-4c7f-88fa-60fa01dc808b"  # windy #todo for several apps

    # ONESIGNAL_KEY: str
    # APP_ID: str

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_queue: str

    @property
    def rabbit_url(self):
        return (
            f'amqp://{self.rabbitmq_default_user}:'
            f'{self.rabbitmq_default_pass}@{self.rabbitmq_host}:'
            f'{self.rabbitmq_port}/'
        )

    clickhouse_host: str
    clickhouse_db: str

    @property
    def clickhouse_url(self):
        return f'http://{self.clickhouse_host}:8123/{self.clickhouse_db}'

    mysql_host: str
    mysql_database: str
    mysql_user: str
    mysql_root_password: str
    mysql_port: int

    @property
    def mysql_url(self):
        return f'mysql+asyncmy://{self.mysql_user}:{self.mysql_root_password}@{self.mysql_host}:3306/{self.mysql_database}'

    celerybeat_schedule = {
        'start_ETL': {
            'task': 'run_distributor.main',
            'schedule': 3.0,
            'options': {
                'expires': 15.0,
            },
        }
    }

    broker_url: str
    single_beat_identifier: str
    single_beat_redis_server: str

    class Config:
        env_file = ENV_FILE


@lru_cache()
def get_settings():
    return Settings()

