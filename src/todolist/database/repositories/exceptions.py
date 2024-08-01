from todolist.exceptions.base import BaseAppException


class NotFoundException(BaseAppException): ...


class InvalidStatusException(BaseAppException): ...
