from celery import Celery
from core.logger import get_logger
from celery_app.settings import get_settings

settings = get_settings()
logger = get_logger(settings.log_filename)

app = Celery(
  broker=settings.broker_url,
  include=['tasks'])

app.conf.beat_schedule = {
        'start_distributor': {
            'task': 'start_distributor',
            'schedule': 3.0,
            'options': {
                'expires': 15.0,
            },
        },
        'start_ETL': {
            'task': 'run_etl.main',
            'schedule': 3.0,
            'options': {
                'expires': 15.0,
            },
        }
}
