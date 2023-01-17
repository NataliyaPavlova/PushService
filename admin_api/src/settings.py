from pathlib import Path
from pydantic import BaseSettings
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename: str = 'logs/admin.log'
    log_level: str = 'INFO'

    clickhouse_host: str
    clickhouse_db: str

    mysql_host: str
    mysql_database: str
    mysql_port: int
    mysql_user: str
    mysql_root_password: str

    @property
    def clickhouse_url(self):
        return f'http://{self.clickhouse_host}:8123/{self.clickhouse_db}'

    @property
    def mysql_url(self):
        return f'mysql+asyncmy://{self.mysql_user}:{self.mysql_root_password}@{self.mysql_host}:3306/{self.mysql_database}'

    class Config:
        env_file = ENV_FILE


@lru_cache()
def get_settings():
    return Settings()
