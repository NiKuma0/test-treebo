from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class BaseRepository:
    _sessionmaker: async_sessionmaker[AsyncSession]

    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker
