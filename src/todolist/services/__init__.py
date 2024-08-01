from aiogram import Bot

from todolist.database.repositories import RepositoriesStore
from todolist.settings import Settings

from .base_service import BaseService


class ServicesStore:
    def __init__(
        self,
        repo_store: RepositoriesStore,
        settings: Settings,
        bot: Bot,
    ) -> None:
        pass


__all__ = (
    "BaseService",
)
