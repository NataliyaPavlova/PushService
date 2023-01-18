from core.logger import get_logger
from core.queue.connection import get_rabbitmq_connection
from core.queue.models import Event
from core.settings import get_settings
from pika import connection, BasicProperties, spec

settings = get_settings()
logger = get_logger(settings.log_filename)


class RabbitSender:

    def __init__(self, connection: connection = get_rabbitmq_connection()) -> None:
        self.connection = connection
        self.channel = connection.channel()
        self.queue = self.channel.queue_declare(
            queue=settings.rabbitmq_queue,
            durable=True
        )

    def publish(self, event: Event) -> None:
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=settings.rabbitmq_queue,
                body=event.json(),
                properties=BasicProperties(
                    delivery_mode=spec.PERSISTENT_DELIVERY_MODE
                )
            )
        except Exception as err:
            logger.error("ERROR: error publishing " + str(err))
            raise err

    def stop(self):
        self.channel.close()
        self.connection.close()
