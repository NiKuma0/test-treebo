import asyncio
import typing as t
import abc
import datetime

from aiogram import Bot

from todolist.clients.exceptions import BackToTheFuture


type DelayType = int | float | datetime.timedelta | datetime.datetime


class MessageData(t.TypedDict):
    chat_id: int | str
    text: str


class ScheduledNotificationAbc(abc.ABC):
    @abc.abstractmethod
    async def send_message(
        self, delay: DelayType, **message: t.Unpack[MessageData]
    ) -> None: ...
    async def shutdown(self): ...


class AsyncScheduledNotification(ScheduledNotificationAbc):
    """Scheduling by asyncio tasks."""

    def __init__(self, bot: Bot):
        self._tasks: set[asyncio.Task[None]] = set()
        self._bot = bot

    async def _send_message_after_delay(
        self, seconds: int | float, **message: t.Unpack[MessageData]
    ):
        try:
            await asyncio.sleep(seconds)
        except asyncio.CancelledError:
            return
        await self._bot.send_message(**message)

    @t.override
    async def send_message(self, delay: DelayType, **message: t.Unpack[MessageData]):
        seconds: int | float
        match delay:
            case datetime.timedelta():
                seconds = delay.total_seconds()
            case datetime.datetime():
                seconds = (delay - datetime.datetime.now()).total_seconds()
            case _:
                seconds = delay
        if seconds < 0:
            raise BackToTheFuture("Notifications into the past are not possible.")
        task = asyncio.create_task(self._send_message_after_delay(seconds, **message))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    @t.override
    async def shutdown(self):
        for task in self._tasks:
            task.cancel()
