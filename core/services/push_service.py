from core.db_mysql.models import Push
from core.db_mysql.repository.push_repository import PushRepository


class PushService:

    def __init__(self, push_repository: PushRepository):
        self.push_repository = push_repository

    async def get(self, push_id: int) -> Push | None:
        return await self.push_repository.get_or_none(push_id)
