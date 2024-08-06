import datetime as dt
import typing as t

from sqlalchemy import orm
import sqlalchemy as sa

from .base_entity import BaseEntity, BaseEntityKw

if t.TYPE_CHECKING:
    from .user_entity import UserEntity


class NoteEntityKw(BaseEntityKw):
    text: str
    remainder_time: dt.datetime

    user: t.NotRequired['UserEntity | None']
    user_id: t.NotRequired[int | None]


class NoteEntity(BaseEntity):
    __tablename__ = 'notes'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    text: orm.Mapped[str] = orm.mapped_column(sa.TEXT)
    remainder_time: orm.Mapped[dt.datetime]

    user_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey('users.id'))
    user: orm.Mapped['UserEntity | None'] = orm.relationship(back_populates='notes')

    if t.TYPE_CHECKING:
        def __init__(self, **kwargs: t.Unpack[NoteEntityKw]): ...
