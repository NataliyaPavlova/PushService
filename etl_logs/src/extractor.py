import http
from typing import AsyncGenerator
import requests

from core.db_mysql.db import get_mysql_session
from core.utils import get_batch_service_callback
from etl_logs.logger import get_logger
from etl_logs.settings import get_settings

settings = get_settings()
logger = get_logger(settings.log_filename)


class OneSignalAPI:
    """Class to deal with OneSignal"""
    # https://documentation.onesignal.com/reference/view-notification

    def __init__(self):
        self.url = settings.onesignal_url
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"{settings.onesignal_key}"
        }

    def view_notification(self, notification_id: str) -> tuple:
        """ View general stats for a notification"""
        url = f"{self.url}/{notification_id}?app_id={settings.app_id}"
        result = requests.get(url, headers=self.headers)
        if result.status_code != http.HTTPStatus.OK:
            return None, None
        body = result.json()
        completed_at = '' if not body['completed_at'] else body['completed_at']
        event_list = [
            {'event': 'remaining', 'number_of_events': 0 if not body['remaining'] else body['remaining'], 'completed_at': completed_at},
            {'event': 'received', 'number_of_events': 0 if not body['received'] else body['received'], 'completed_at': completed_at},
            {'event': 'errored', 'number_of_events': 0 if not body['errored'] else body['errored'], 'completed_at': completed_at},
            {'event': 'successful', 'number_of_events': 0 if not body['successful'] else body['successful'], 'completed_at': completed_at},
            {'event': 'converted', 'number_of_events': 0 if not body['converted'] else body['converted'], 'completed_at': completed_at},
            {'event': 'failed', 'number_of_events': 0 if not body['failed'] else body['failed'], 'completed_at': completed_at}
        ]
        return event_list, body['include_player_ids']


class Extractor:
    """Class to extract logs from OneSignal"""

    def __init__(self):
        self.onesignal = OneSignalAPI()

    async def get_data(self) -> AsyncGenerator:
        logger.info('Start getting logs from OneSignal')

        session = get_mysql_session()
        batch_service = await get_batch_service_callback(session)

        batches = await batch_service.get_batches_to_log()
        for batch in batches:
            batch_logs, push_tokens = self.onesignal.view_notification(batch.notification_id)
            await batch_service.set_status_logged(batch.id)
            yield batch_logs, batch, push_tokens

