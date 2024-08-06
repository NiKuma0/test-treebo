from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


def get_engine(db_dsn: str = "sqlite+aiosqlite:///database.sqllite") -> AsyncEngine:
    return create_async_engine(db_dsn)


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
