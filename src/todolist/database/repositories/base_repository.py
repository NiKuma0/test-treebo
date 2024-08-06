import typing as t

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import abc

type SessionMakerType[T] = t.Callable[..., t.AsyncContextManager[T]]


class AbcRepository[T: SessionMakerType[t.Any]](abc.ABC):
    _sessionmaker: T

    def __init__(self, sessionmaker: T):
        self._sessionmaker = sessionmaker


class BaseRepository(AbcRepository[async_sessionmaker[AsyncSession]]):
    _sessionmaker: async_sessionmaker[AsyncSession]
