from typing import Iterable
import datetime

from core.db_clickhouse.db import get_clickhouse_client
from core.db_mysql.models import Batch
from core.db_clickhouse.models import Log
from etl_logs.logger import get_logger
from etl_logs.settings import get_settings
from core.utils import get_stats_service_callback

settings = get_settings()
logger = get_logger(settings.log_filename)


class Loader:

    async def load_data(self, data: Iterable[dict], batch_info: Batch, push_tokens: list) -> None:
        client = get_clickhouse_client()
        stats_service = await get_stats_service_callback(client)

        prepared_data = self.prepare_data(data, batch_info, push_tokens)
        await stats_service.insert(prepared_data)

    @staticmethod
    def prepare_data(raw_data: Iterable[dict], batch_info: Batch, push_tokens: list) -> str:
        rows = []
        for row in raw_data:
            row_validated = Log(
                push_tokens=push_tokens,
                created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                completed_at=row['completed_at'],
                event=row['event'],
                number_of_events=row['number_of_events'],
                notification_id=batch_info.notification_id,
                campaign_id=batch_info.campaign_id,
                push_id=batch_info.push_id
            )

            r_string = (
              row_validated.push_tokens, row_validated.created_at, row_validated.completed_at,
              row_validated.dict()['event'], row_validated.number_of_events, row_validated.notification_id,
              row_validated.campaign_id, row_validated.push_id
            )
            rows.append(r_string)
        return str(rows).strip('[]')

