from aiochclient import ChClient
from aiohttp import ClientSession

from core.settings import get_settings


async def get_clickhouse_client() -> ChClient:
    settings = get_settings()
    async with ClientSession() as s:
        client = ChClient(s, url=settings.clickhouse_url)
        yield client
