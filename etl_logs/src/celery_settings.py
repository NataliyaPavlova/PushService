from celery_settings import Celery

app = Celery()
app.config_from_object('etl_logs.settings.CelerySettings')
