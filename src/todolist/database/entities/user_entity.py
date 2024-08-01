import typing as t

from sqlalchemy import orm
from sqlalchemy import BigInteger

from .base_entity import BaseEntity

if t.TYPE_CHECKING:
    from .todo_entity import ToDoEntity


class UserEntity(BaseEntity):
    __tablename__ = "users"

    telegram_id: orm.Mapped[int] = orm.mapped_column(BigInteger)
    email: orm.Mapped[str]
    name: orm.Mapped[str]

    todos: orm.Mapped[list['ToDoEntity']]
