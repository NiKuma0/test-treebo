import typing as t

from todolist.database.entities import UserEntity
from todolist.database.repositories.types import UserCreateValues

from .base_service import BaseService


class UserService(BaseService):
    async def get_or_none(self, telegram_id: int) -> UserEntity | None:
        return await self._repo_store.user_repo.get_by_telegram_id(telegram_id)

    async def register(self, **user: t.Unpack[UserCreateValues]) -> UserEntity:
        return await self._repo_store.user_repo.get_or_create(**UserCreateValues(user))
