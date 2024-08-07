import typing as t

from aiogram import Bot

from todolist.database.entities import NoteEntity
from todolist.database.repositories.types import NoteCreateValues
from todolist.clients import ScheduledNotificationAbc
from todolist.settings import Settings

from .base_service import BaseService, IRepositoriesStore


class NoteService(BaseService):
    def __init__(
        self,
        repo_store: IRepositoriesStore,
        settings: Settings,
        bot: Bot,
        schedule_client: ScheduledNotificationAbc,
    ) -> None:
        super().__init__(repo_store, settings, bot)
        self._schedule_client = schedule_client

    async def create(
        self, chat_id: int, **note: t.Unpack[NoteCreateValues]
    ) -> NoteEntity:
        await self._schedule_client.send_message(
            note["remainder_time"], chat_id=chat_id, text=note["text"]
        )
        return await self._repo_store.note_repo.create(**note)

    async def get_my_notes(self, user_id: int):
        return await self._repo_store.note_repo.get_my_notes(user_id)
