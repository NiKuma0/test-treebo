import typing as t
from aiogram import Bot

from todolist.settings import Settings
from todolist.database.repositories import AbcNoteRepository, AbcUserRepository


class IRepositoriesStore(t.Protocol):
    @property
    def user_repo(self) -> AbcUserRepository: ...
    @property
    def note_repo(self) -> AbcNoteRepository: ...


class BaseService:
    _repo_store: IRepositoriesStore

    def __init__(
        self, repo_store: IRepositoriesStore, settings: Settings, bot: Bot
    ) -> None:
        self._settings = settings
        self._repo_store = repo_store
        self._bot = bot
