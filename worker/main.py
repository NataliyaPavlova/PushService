import asyncio
import json
from typing import Any
import time
import requests as requests
import os
import sys
from pathlib import Path

import aio_pika

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(os.path.dirname(BASE_DIR))

from core.logger import get_logger
from core.queue.connection import get_async_rabbitmq_connection
from core.queue.models import Event
from core.settings import get_settings
from core.db_mysql.models import Batch
from core.services.batch_service import BatchService
from core.services.campaign_service import CampaignService
from core.services.push_service import PushService
from core.utils import get_batch_campaign_push_service_callback
from core.db_mysql.db import get_mysql_session


settings = get_settings()
logger = get_logger(settings.log_filename)

HEADERS = {"Content-Type": "application/json; charset=utf-8",
           "Authorization": settings.onesignal_key}


class WorkerPublisher:

    def __init__(self, batch_service: BatchService, campaign_service: CampaignService, push_service: PushService):
        self.campaign_service = campaign_service
        self.push_service = push_service
        self.batch_service = batch_service
        self.queue = None
        self.processed_batches = []

    async def set_queue_callbacks(self) -> None:
        # channel.basic_qos(prefetch_count=10)
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.callback(message.body)

        await asyncio.Future()

    async def create_queues(self, channel: aio_pika.Channel) -> None:
        self.queue = await channel.declare_queue(settings.rabbitmq_queue, durable=True)

    async def get_push_data(self, event: Event) -> dict | None:
        batch = await self.batch_service.get(event.batch_id)
        push = await self.push_service.get(event.push_id)
        push_tokens = await self.batch_service.get_push_tokens(batch.id)
        if not push:
            return

        payload = {
            "app_id": settings.app_id,
            "include_player_ids": push_tokens,
            "contents": push.contents,
            "headings": push.headings,
            "data": push.data,
            "priority": 10
        }
        return payload

    async def callback(self, body: Any) -> None:
        event = Event(**json.loads(body))
        logger.info(f'Sending batch {event.batch_id} with push_id {event.push_id}')
        batch = await self.batch_service.get(event.batch_id)
        payload = await self.get_push_data(event)
        req = requests.post(settings.onesignal_url, headers=HEADERS,
                            data=json.dumps(payload))

        if req.status_code == 200 and req.json()['id']:
            batch.status = Batch.BatchStatus.SENT.value
            batch.notification_id = req.json()['id']
            logger.info(f'Successfully sent batch {event.batch_id} to OneSignal with {batch.notification_id=}')
        else:
            batch.status = Batch.BatchStatus.REJECTED.value
            logger.info(f'Batch {event.batch_id} was rejected with the following status_code: {req.status_code} and errors: {req.json()["errors"]}. Body: {req.json()}')
            # TODO deal with invalid_player_ids in errors

        await self.batch_service.update(batch)

        time.sleep(2)


async def start_worker():
    session = get_mysql_session()
    batch_service, campaign_service, push_service = await get_batch_campaign_push_service_callback(session)
    rabbit_connection = await get_async_rabbitmq_connection()
    rabbit_channel = await rabbit_connection.channel()

    worker = WorkerPublisher(batch_service, campaign_service, push_service)
    await worker.create_queues(rabbit_channel)
    await worker.set_queue_callbacks()
    logger.info('Rabbit callback initialized')
    logger.info('Waiting for messages.')

if __name__ == "__main__":
    asyncio.run(start_worker())
