from abc import ABC

from core.db_clickhouse.repository.stats_repository import StatsRepository
from core.db_mysql.repository.batch_repository import BatchRepository
from core.db_mysql.repository.push_repository import PushRepository
from core.db_mysql.repository.campaign_repository import CampaignRepository


class AbstractService(ABC):
    def __init__(self) -> None:
        self.push_repository = PushRepository()
        self.campaign_repository = CampaignRepository()
        self.batch_repository = BatchRepository()
        self.stats_repository = StatsRepository()
