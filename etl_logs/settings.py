from pathlib import Path
from pydantic import BaseSettings
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = str(BASE_DIR / '.env')


class Settings(BaseSettings):
    log_filename: str = 'logs/etl.log'
    log_level: str = 'INFO'

    clickhouse_host: str
    clickhouse_port: int
    clickhouse_db: str
    clickhouse_user: str
    clickhouse_password: str

    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_root_password: str

    onesignal_key: str
    onesignal_url: str
    app_id: str

    @property
    def clickhouse_url(self):
        return f'http://{self.clickhouse_user}:{self.clickhouse_password}@{self.clickhouse_host}:{self.clickhouse_port}/{self.clickhouse_db}'

    @property
    def mysql_url(self):
        return f'mysql+asyncmy://{self.mysql_user}:{self.mysql_root_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}'

    class Config:
        env_file = ENV_FILE

@lru_cache()
def get_settings():
    return Settings()

