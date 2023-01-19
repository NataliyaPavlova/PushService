from core.services.campaign_service import CampaignService
from core.services.batch_service import BatchService
from core.services.stats_service import StatsService
from core.services.push_service import PushService

from core.db_mysql.repository.campaign_repository import CampaignRepository
from core.db_mysql.repository.push_repository import PushRepository
from core.db_mysql.repository.batch_repository import BatchRepository
from core.db_mysql.repository.user_batch_repository import UserBatchRepository
from core.db_clickhouse.repository.stats_repository import StatsRepository


async def get_campaign_service_callback(sessions):
    async for session in sessions:
        campaign_repository = CampaignRepository(session)
        push_repository = PushRepository(session)
        campaign_service = CampaignService(campaign_repository, push_repository)
        return campaign_service


async def get_batch_campaign_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        campaign_repository = CampaignRepository(session)
        user_batch_repository = UserBatchRepository(session)
        push_repository = PushRepository(session)
        batch_service = BatchService(batch_repository, user_batch_repository, campaign_repository)
        campaign_service = CampaignService(campaign_repository, push_repository)
        return batch_service, campaign_service


async def get_batch_campaign_push_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        campaign_repository = CampaignRepository(session)
        user_batch_repository = UserBatchRepository(session)
        push_repository = PushRepository(session)
        batch_service = BatchService(batch_repository, user_batch_repository, campaign_repository)
        campaign_service = CampaignService(campaign_repository, push_repository)
        push_service = PushService(push_repository)
        return batch_service, campaign_service, push_service


async def get_batch_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        campaign_repository = CampaignRepository(session)
        user_batch_repository = UserBatchRepository(session)
        batch_service = BatchService(batch_repository, user_batch_repository, campaign_repository)
        return batch_service


async def get_stats_service_callback(sessions):
    async for session in sessions:
        stats_repository = StatsRepository(session)
        stats_service = StatsService(stats_repository)
        return stats_service
