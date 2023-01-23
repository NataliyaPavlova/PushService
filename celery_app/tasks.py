import asyncio

from celery_app.celery_worker import app
from distributor.main import start_distributor
from etl_logs.main import make_etl


@app.task
def distributor_task():
    asyncio.run(start_distributor())


@app.task
def etl_task():
    asyncio.run(make_etl())
