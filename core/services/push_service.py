from core.db_mysql.models import Push
from core.services.abstract_service import AbstractService


class PushService(AbstractService):

    def get(self, push_id: int) -> Push | None:
        return self.push_repository.get_or_none(push_id)
