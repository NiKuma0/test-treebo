import datetime
import typing as t


class UserCreateValues(t.TypedDict):
    name: str
    email: str
    telegram_id: int


class NoteCreateValues(t.TypedDict):
    text: str
    user_id: int
    remainder_time: datetime.datetime
