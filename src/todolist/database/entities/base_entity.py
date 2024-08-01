from sqlalchemy import orm


class BaseEntity(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
