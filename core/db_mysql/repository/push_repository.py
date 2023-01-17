from core.db_mysql.models import Push

from core.db_mysql.repository.abstract_repository import AbstractMysqlRepository


class PushRepository(AbstractMysqlRepository):
    model = Push
