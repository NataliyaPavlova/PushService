import asyncio

from celery_app.celery_worker import app
from distributor.main import start_distributor


@app.task(bind=True, name='start_distributor')
def distributor_task():
    asyncio.run(start_distributor())
