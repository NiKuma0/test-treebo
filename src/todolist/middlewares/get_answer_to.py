import typing as t

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from todolist.utils import (
    AnswerToMessage,
    AnswerToAbc,
    AnswerToNotImplemented,
    AnswerToCallbackQuery,
)


class AnswerToMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: t.Callable[[TelegramObject, dict[str, t.Any]], t.Awaitable[t.Any]],
        event: TelegramObject,
        data: dict[str, t.Any],
    ) -> t.Any:
        answer_to: AnswerToAbc

        match event:
            case Message():
                answer_to = AnswerToMessage(event)
            case CallbackQuery():
                answer_to = AnswerToCallbackQuery(event, data["bot"])
            case _:
                answer_to = AnswerToNotImplemented(event)

        data["answer_to"] = answer_to
        return await handler(event, data)
