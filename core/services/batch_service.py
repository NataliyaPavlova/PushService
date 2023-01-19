import math
from typing import Sequence

from core.db_mysql.models import Batch, Campaign
from core.logger import get_logger
from core.queue.models import Event
from core.settings import get_settings
from core.db_mysql.repository.batch_repository import BatchRepository
from core.db_mysql.repository.campaign_repository import CampaignRepository
from core.db_mysql.repository.user_batch_repository import UserBatchRepository

MAX_TOTAL_USERS_IN_BATCH = 2

logger = get_logger(get_settings().log_filename)


class BatchService:

    def __init__(self,
                 batch_repository: BatchRepository,
                 user_batch_repository: UserBatchRepository,
                 campaign_repository: CampaignRepository):
        self.batch_repository = batch_repository
        self.user_batch_repository = user_batch_repository
        self.campaign_repository = campaign_repository

    async def distribute_users_on_batch(self, campaign: Campaign, users: list) -> None:
        """Create and save batches to db, distribute users by batches"""
        total_users = len(users)

        number_of_batches = math.ceil(total_users/MAX_TOTAL_USERS_IN_BATCH)
        logger.info(f'{total_users=}, {number_of_batches=}')

        users_list_position = 0

        batches = []
        for _ in range(number_of_batches):
            batch = Batch(
                campaign_id=campaign.id,
                push_id=campaign.push_id,
                status=Batch.BatchStatus.NEW.value,
            )
            batch = await self.batch_repository.create(batch)
            batches.append(batch)

            if users_list_position + MAX_TOTAL_USERS_IN_BATCH < total_users:
                user_batch = users[users_list_position:users_list_position + MAX_TOTAL_USERS_IN_BATCH]
                users_list_position += MAX_TOTAL_USERS_IN_BATCH
            else:
                user_batch = users[users_list_position:]
            await self.user_batch_repository.add_users(batch, user_batch)

            logger.info(f'Saves {len(batches)} batches in DB.')

        campaign.status = Campaign.CampaignStatus.STARTED.value
        await self.campaign_repository.update(campaign)
        logger.info(f'Distributed {users_list_position} users from {total_users}')

    async def get_campaign_to_send(self) -> Sequence[Campaign]:
        return await self.campaign_repository.list(status=Campaign.CampaignStatus.STARTED)

    async def get_batches_for_send(self, campaign_id: int) -> list[Batch]:
        return await self.batch_repository.get_batches(
            status=Batch.BatchStatus.NEW.value,
            campaign_id=campaign_id,
        )

    async def get(self, batch_id: int) -> Batch:
        return await self.batch_repository.get_or_none(batch_id)

    async def get_push_tokens(self, batch_id: int) -> list[str]:
        return await self.user_batch_repository.get_user_push_tokens(batch_id)
    #
    # def get_batches_to_log(self) -> list[Batch] | None:
    #     return self.batch_repository.get_batches_to_log()
    #
    # def set_status_logged(self, batch_id) -> Batch:
    #     batch = self.batch_repository.get(batch_id)
    #     batch.status = Batch.BatchStatus.LOGGED
    #     return self.batch_repository.update(batch)

    async def update(self, batch) -> None:
        await self.batch_repository.update(batch)
