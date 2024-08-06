from aiogram import Bot

from todolist.clients.scheduled_notification_client import ScheduledNotificationAbc
from todolist.settings import Settings

from .base_service import BaseService, IRepositoriesStore
from .user_service import UserService
from .note_service import NoteService


class ServicesStore:
    def __init__(
        self,
        repo_store: IRepositoriesStore,
        settings: Settings,
        bot: Bot,
        schedule_client: ScheduledNotificationAbc
    ) -> None:
        self.user_service = UserService(repo_store, settings, bot)
        self.note_service = NoteService(repo_store, settings, bot, schedule_client)


__all__ = (
    "BaseService",
    "UserService",
    "NoteService",
)
