import datetime
import typing as t

from sqlalchemy import orm
import sqlalchemy as sa

from .base_entity import BaseEntity

if t.TYPE_CHECKING:
    from .user_entity import UserEntity


class ToDoEntity(BaseEntity):
    text: orm.Mapped[str] = orm.mapped_column(sa.TEXT)
    remainder_time: orm.Mapped[datetime.datetime]

    user_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user: orm.Mapped['UserEntity'] = orm.relationship(back_populates='todos')
