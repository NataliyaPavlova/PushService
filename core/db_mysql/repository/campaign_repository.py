from typing import Sequence

from sqlalchemy import select, func

from core.db_mysql.models import Campaign, Push
from core.db_mysql.repository.abstract_repository import AbstractMysqlRepository


class CampaignRepository(AbstractMysqlRepository):
    model = Campaign

    async def list(self, status: Campaign.CampaignStatus) -> Sequence[Campaign]:
        stmt = select(self.model). \
            select_from(self.model). \
            where(self.model.status == status.value)
        res = await self.session.execute(stmt)
        data = res.scalars().all()
        await self.session.commit()
        return data

