import abc
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from core.db_mysql.db import get_mysql_session
from core.db_mysql.models import Base

MESSAGE_NO_ITEM = 'No objects found by the id provided'


class AbstractMysqlRepository(abc.ABC):
    """Storage class to follow the Repository pattern"""
    model: type[Base] = None

    def __init__(self, session: AsyncSession = get_mysql_session()) -> None:
        self.session = session

    async def get_or_none(self, _id: int) -> Base | None:
        """Get an object from DB by id. If no object found - return None"""
        instance = await self.session.get(self.model, _id)
        if instance:
            return instance
        return None

    async def update(self, instance: type[Base]) -> type[Base]:
        """Save a new object in DB. Returns the object"""
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def create(self, instance: type[Base]) -> type[Base]:
        """Save a new object in DB. Returns the object"""
        self.session.add(instance)
        await self.session.commit()
        # await self.session.refresh(instance)
        return instance



