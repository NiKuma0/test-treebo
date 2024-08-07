import typing as t
import abc

import sqlalchemy as sa
from sqlalchemy.sql import func

from todolist.database.entities.note_entity import NoteEntity

from .types import NoteCreateValues
from .base_repository import BaseRepository


class AbcNoteRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, **values: t.Unpack[NoteCreateValues]) -> NoteEntity: ...
    @abc.abstractmethod
    async def get_my_notes(self, user_id: int) -> t.Sequence[NoteEntity]: ...


class NoteRepository(BaseRepository, AbcNoteRepository):
    @t.override
    async def create(self, **values: t.Unpack[NoteCreateValues]) -> NoteEntity:
        q = sa.insert(NoteEntity).values(**values).returning(NoteEntity)
        async with self._sessionmaker() as session:
            res = await session.execute(q)
        return res.scalar_one()

    @t.override
    async def get_my_notes(self, user_id: int) -> t.Sequence[NoteEntity]:
        q = (
            sa.select(NoteEntity)
            .where(NoteEntity.user_id == user_id)
            .where(NoteEntity.remainder_time > func.now())
            .order_by(NoteEntity.remainder_time)
        )
        async with self._sessionmaker() as session:
            res = await session.scalars(q)
            await session.commit()
        return res.all()
