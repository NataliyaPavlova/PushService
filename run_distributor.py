import asyncio
from celery import shared_task
import time

from core.logger import get_logger
from core.settings import get_settings
from distributor.main import start_distributor

settings = get_settings()
logger = get_logger(settings.log_filename)

if __name__ == "__main__":
    asyncio.run(start_distributor())
