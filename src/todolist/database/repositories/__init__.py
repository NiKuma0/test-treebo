from contextlib import asynccontextmanager

from todolist.database.entities import BaseEntity

from .base_repository import BaseRepository
from .user_repository import UserRepository
from .note_repository import NoteRepository

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class RepositoriesStore:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker
        self.user_repo = UserRepository(sessionmaker)
        self.note_repo = NoteRepository(sessionmaker)

    async def add_to_session_and_commit(self, entity: BaseEntity):
        async with self._sessionmaker() as session:
            session.add(entity)
            await session.commit()

    @asynccontextmanager
    async def transaction(self):
        async with self._sessionmaker().begin() as transaction:
            yield transaction


__all__ = (
    "BaseRepository",
    "UserRepository",
)