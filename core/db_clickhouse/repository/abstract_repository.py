from abc import ABC
from typing import Any
from uuid import UUID

from aiochclient import ChClient

from core.db_clickhouse.db import get_clickhouse_client
from core.db_clickhouse.models import Log

MESSAGE_NO_ITEM = 'No objects found by the id provided'


class AbstractRepositoryClickHouse(ABC):
    """Abstract class to follow the Repository pattern"""

    def __init__(self, client: ChClient = get_clickhouse_client()) -> None:
        self.client = client
        self.model = Log

    async def get_or_none(self, _id: UUID) -> Any | None:
        """Get an object from DB by id. If no object found - return None"""
        if not _id:
            return None
        if isinstance(_id, UUID):
            return await self.client.fetchrow(
                "SELECT * FROM {model} WHERE id={id}",
                params={'model': self.model, 'id': _id})
        return None

    async def get(self, _id: UUID) -> Any | None:
        """Get an object from DB by id. If no object found - raises exception"""
        instance = await self.client.fetchrow(
            "SELECT * FROM {model} WHERE id={id}",
            params={'model': self.model, 'id': _id})
        if not instance:
            raise LookupError("No objects found by the id provided")
        return instance

    async def create(self, instance: Any) -> Any:
        pass
