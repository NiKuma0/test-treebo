import typing as t

from sqlalchemy import orm
from sqlalchemy import BigInteger

from .base_entity import BaseEntity, BaseEntityKw

if t.TYPE_CHECKING:
    from .note_entity import NoteEntity


class UserEntityKw(BaseEntityKw):
    telegram_id: int
    email: str
    name: str

    notes: t.NotRequired[list['NoteEntity'] | None]

class UserEntity(BaseEntity):
    __tablename__ = "users"

    telegram_id: orm.Mapped[int] = orm.mapped_column(BigInteger)
    email: orm.Mapped[str]
    name: orm.Mapped[str]

    notes: orm.Mapped[list['NoteEntity'] | None] = orm.relationship()

    if t.TYPE_CHECKING:
        def __init__(self, **kwargs: t.Unpack[UserEntityKw]): ...
