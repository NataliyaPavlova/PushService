from functools import lru_cache
import aio_pika
from pika import URLParameters, BlockingConnection

from core.settings import get_settings

settings = get_settings()
parameters = URLParameters(settings.rabbit_url)


@lru_cache
def get_rabbitmq_connection() -> BlockingConnection:
    connection = BlockingConnection(parameters)
    return connection


@lru_cache
async def get_async_rabbitmq_connection() -> aio_pika.Connection:
    connection = await aio_pika.connect_robust(
        settings.rabbit_url)
    return connection
    # async with connection:
    #     yield connection
