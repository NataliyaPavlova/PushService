from celery import Celery
from celery.schedules import crontab
from core.logger import get_logger
from celery_app.settings import get_settings

settings = get_settings()
logger = get_logger(settings.log_filename)

app = Celery(
  broker=settings.broker_url,
  include=['celery_app.tasks'])

app.conf.beat_schedule = {
        'start_distributor': {
            'task': 'celery_app.tasks.distributor_task',
            'schedule': crontab(minute='*/5'),
        },
        'start_ETL': {
            'task': 'celery_app.tasks.etl_task',
            'schedule': crontab(minute='*/60')
        }
}
