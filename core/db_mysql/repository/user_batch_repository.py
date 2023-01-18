from sqlalchemy.future import select
from core.db_mysql.models import UserBatch, Batch
from core.db_mysql.repository.abstract_repository import AbstractMysqlRepository


class UserBatchRepository(AbstractMysqlRepository):
    model = UserBatch

    async def add_users(self, batch: Batch, user_batch: list) -> None:
        data = []
        for user_batch_item in user_batch:
            data.append(UserBatch(batch_id=batch.id, push_token_id=user_batch_item))
        self.session.add_all(data)
        await self.session.commit()

    async def get_user_push_tokens(self, batch_id: int) -> list[str]:
        stmt = select(UserBatch.push_token_id). \
            where(UserBatch.batch_id == batch_id)

        res = await self.session.execute(stmt)
        users = res.scalars().all()
        await self.session.commit()
        return users


