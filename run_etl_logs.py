import asyncio
import time

from core.logger import get_logger
from core.settings import get_settings
from etl_logs.main import make_etl

settings = get_settings()
logger = get_logger(settings.log_filename)


if __name__ == "__main__":
    while True:
        asyncio.run(make_etl())
        time.sleep(10)

