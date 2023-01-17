from celery import shared_task, Celery

from core.logger import get_logger
from core.settings import get_settings
from worker.main import start_worker

settings = get_settings()
logger = get_logger(settings.log_filename)

app = Celery()
app.config_from_object('core.settings.CelerySettings')
app.conf.beat_schedule = {
    'send_new_notifications': {
        'task': 'run_worker.main',
        'schedule': 5,
    },
}


@shared_task
def main():
    start_worker()


if __name__ == "__main__":
    start_worker()
