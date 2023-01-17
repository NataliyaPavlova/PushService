import json
from typing import Any
import time
import requests as requests

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from core.logger import get_logger
from core.queue.connection import get_rabbit_channel
from core.queue.models import Event
from core.queue.rabbit_sender import RabbitSender
from core.settings import get_settings
from core.db_mysql.models import Batch
from core.services.batch_service import BatchService
from core.services.campaign_service import CampaignService
from core.services.cohort_service import CohortService
from core.services.push_service import PushService
from core.services.user_service import UserService

settings = get_settings()
logger = get_logger(settings.log_filename)

campaign_service = CampaignService()
push_service = PushService()
cohort_service = CohortService()
queue_repository = RabbitSender()

user_service = UserService()
batch_service = BatchService()

HEADERS = {"Content-Type": "application/json; charset=utf-8",
           "Authorization": settings.onesignal_key}


def set_queue_callbacks(channel: BlockingChannel) -> None:
    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=callback)


def create_queues(channel: BlockingChannel) -> None:
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)


def send_messages() -> None:
    pass


def callback(channel: BlockingChannel, method_frame: Basic.Deliver, properties: Any,
             body: Any) -> None:
    event = Event(**json.loads(body))

    batch = batch_service.get(event.batch_id)
    push = push_service.get(event.push_id)
    logger.info(f'Sending batch {event.batch_id} with push_id {event.push_id}')
    push_tokens = batch_service.get_push_tokens(batch.id)
    if not push:
        return

    payload = {
        "app_id": settings.app_id,
        "include_player_ids": push_tokens,
        "contents": push.contents,
        "headings": push.headings,
        "data": {"type": "PushBuyPro"},
        "send_after": batch.send_after.timestamp(),
        "delayed_option": "timezone",
        "delivery_time_of_day": '18:00',  #todo from admin_api
        "ttl": 86400,
    }

    req = requests.post(settings.onesignal_url, headers=HEADERS,
                        data=json.dumps(payload))

    if req.status_code == 200 and req.json()['id']:
        batch.status = Batch.BatchStatus.SENT.value
        notification_id = req.json()['id']
        batch.notification_id = notification_id
        logger.info(f'Successfully sent batch {batch.id} to OneSignal')
    else:
        batch.status = Batch.BatchStatus.REJECTED.value
        logger.info(f'Batch {batch.id} was rejected with the following status_code: {req.status_code}')

    batch_service.update(batch)
    time.sleep(2)
    channel.basic_ack(method_frame.delivery_tag)


def start_worker():
    rabbit_channel = get_rabbit_channel()
    create_queues(rabbit_channel)
    set_queue_callbacks(rabbit_channel)
    logger.info('Rabbit callback initialized')

    logger.info('Waiting for messages.')
    rabbit_channel.start_consuming()

    logger.info('Application closed.')
