import typing as t

from sqlalchemy import orm


class BaseEntityKw(t.TypedDict):
    id: t.NotRequired[int]


class BaseEntity(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    if t.TYPE_CHECKING:

        def __init__(self, **kwargs: t.Unpack[BaseEntityKw]): ...
