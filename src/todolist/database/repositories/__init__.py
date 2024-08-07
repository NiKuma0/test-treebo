import typing as t

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .base_repository import BaseRepository
from .user_repository import UserRepository, AbcUserRepository
from .note_repository import NoteRepository, AbcNoteRepository


class RepositoriesStore:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker
        self._user_repo: t.Final = UserRepository(sessionmaker)
        self._note_repo: t.Final = NoteRepository(sessionmaker)

    @property
    def user_repo(self) -> UserRepository:
        return self._user_repo

    @property
    def note_repo(self) -> NoteRepository:
        return self._note_repo


__all__ = (
    "BaseRepository",
    "UserRepository",
    "AbcUserRepository",
    "AbcNoteRepository",
)
