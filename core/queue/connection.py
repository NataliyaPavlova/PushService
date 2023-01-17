from functools import lru_cache

from pika import URLParameters, BlockingConnection

from core.settings import get_settings

settings = get_settings()
parameters = URLParameters(settings.rabbit_url)
connection = BlockingConnection(parameters)


@lru_cache
def get_rabbitmq_connection() -> BlockingConnection:
    return connection


@lru_cache
def get_rabbit_channel():
    rabbit_channel = connection.channel()
    return rabbit_channel
