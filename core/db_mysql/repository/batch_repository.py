from sqlalchemy.future import select

from core.db_mysql.models import Batch
from core.db_mysql.repository.abstract_repository import AbstractMysqlRepository
from core.settings import get_settings
from core.logger import get_logger

settings = get_settings()
logger = get_logger(settings.log_filename)


class BatchRepository(AbstractMysqlRepository):
    model = Batch

    async def get_all_data_of_batch(self, batch_id: int) -> list[Batch]:
        stmt = select(Batch).select_from(Batch).where(
            Batch.id == batch_id)
        res = await self.session.execute(stmt)
        data = res.scalars().all()
        await self.session.commit()
        return data

    async def get_batches_to_log(self) -> list[Batch]:
        stmt = select(Batch). \
            where(Batch.status == Batch.BatchStatus.SENT.value)

        res = await self.session.execute(stmt)
        batches = res.scalars().all()
        await self.session.commit()
        return batches

    async def get_batches(self, status: str, campaign_id: int) -> list[Batch]:
        stmt = select(Batch). \
            where((Batch.status == status) & (Batch.campaign_id == campaign_id))

        res = await self.session.execute(stmt)
        batches = res.scalars().all()
        await self.session.commit()
        return batches



