from typing import Tuple, Sequence

from core.db_mysql.models import Campaign, Push, CampaignRequestCreate
from core.db_mysql.repository.campaign_repository import CampaignRepository
from core.db_mysql.repository.push_repository import PushRepository


class CampaignService:

    def __init__(self, campaign_repository: CampaignRepository(), push_repository: PushRepository()) -> None:
        self.push_repository = push_repository
        self.campaign_repository = campaign_repository

    async def save_campaign(self, campaign: CampaignRequestCreate) -> Tuple[Campaign, Push]:
        push_status = Push.PushType(campaign.push.push_type)
        created_push = await self.push_repository.create(Push(
            headings=campaign.push.headings,
            contents=campaign.push.contents,
            push_type=push_status.value,
            data=campaign.push.data))
        created_campaign = await self.campaign_repository.create(Campaign(
            started_at=campaign.started_at,
            finished_at=campaign.finished_at,
            status=Campaign.CampaignStatus.PENDING.value,
            push_id=created_push.push_id,
            users=campaign.users,
            app_name=campaign.app_name))
        return created_campaign, created_push

    async def get_pending_campaigns(self) -> Sequence[Campaign]:
        return await self.campaign_repository.list(status=Campaign.CampaignStatus.PENDING)

    async def get_users(self, campaign_id: int) -> list:
        campaign = await self.campaign_repository.get_or_none(campaign_id)
        return campaign.users

    async def get(self, campaign_id: int) -> Campaign:
        return await self.campaign_repository.get_or_none(campaign_id)



