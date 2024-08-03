import typing as t

import sqlalchemy as sa

from todolist.database.entities import UserEntity

from .base_repository import BaseRepository
from .types import UserCreateValues


class UserRepository(BaseRepository):
    async def get_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        q = sa.select(UserEntity).where(UserEntity.telegram_id == telegram_id)
        async with self._sessionmaker() as session:
            return await session.scalar(q)

    async def get_or_create(self, **values: t.Unpack[UserCreateValues]) -> UserEntity:
        user = await self.get_by_telegram_id(values['telegram_id'])
        if user is not None: return user
        q = sa.insert(UserEntity).values(**values).returning(UserEntity)
        async with self._sessionmaker() as session:
            res = await session.execute(q)
            await session.commit()
        return res.scalar_one()
