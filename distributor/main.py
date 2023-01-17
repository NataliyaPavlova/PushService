from core.db_mysql.models import Campaign, Batch
from core.logger import get_logger
from core.queue.rabbit_sender import RabbitSender
from core.settings import get_settings
from core.queue.models import Event
from core.utils import get_campaign_service_callback, get_batch_service_callback
from core.db_mysql.db import get_mysql_session

settings = get_settings()
logger = get_logger(settings.log_filename)

session = get_mysql_session()
campaign_service = await get_campaign_service_callback(session)
batch_service = await get_batch_service_callback(session)

queue_repository = RabbitSender()


async def create_batch_for_campaign(campaign: Campaign):
    users = await campaign_service.get_users(campaign.id)
    logger.info(f'Distribution of {len(users)} of campaign #{campaign.id}...')
    await batch_service.distribute_users_on_batch(campaign, users)


async def add_batches_to_queue(campaign: Campaign) -> None:
    logger.info(f'Adding pushes in queue...')
    batches = await batch_service.get_batches_for_send(campaign.id)
    for batch in batches:
        event = Event(batch_id=batch.id, push_id=batch.push_id)
        batch.status = Batch.BatchStatus.IN_QUEUE
        await batch_service.update(batch)
        queue_repository.publish(event)


async def processing_pending_campaigns() -> None:
    campaigns = await campaign_service.get_pending_campaigns()
    logger.info(f'Found {len(campaigns)} campaigns with status "pending".')

    for campaign in campaigns:
        await create_batch_for_campaign(campaign)
    logger.info(f'Distribution users by batches is completed.')


async def create_events_for_batches() -> None:
    logger.info(f'Start sending notifications.')

    campaigns = await batch_service.get_campaign_to_send()
    logger.info(f'Find batches for {len(campaigns)} campaigns for processing.')
    for campaign in campaigns:
        await add_batches_to_queue(campaign)

    logger.info(f'Sending notifications to queue is completed.')


async def start_distributor():
    await processing_pending_campaigns()
    await create_events_for_batches()
