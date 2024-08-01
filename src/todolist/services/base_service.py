from aiogram import Bot

from todolist.database.repositories import RepositoriesStore
from todolist.settings import Settings


class BaseService:
    _repo_store: RepositoriesStore

    def __init__(
        self, repo_store: RepositoriesStore, settings: Settings, bot: Bot
    ) -> None:
        self._settings = settings
        self._repo_store = repo_store
        self._bot = bot
