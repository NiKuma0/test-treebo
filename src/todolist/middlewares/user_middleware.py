import typing as t

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject, User

from todolist.services import ServicesStore


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: t.Callable[[TelegramObject, dict[str, t.Any]], t.Awaitable[t.Any]],
        event: TelegramObject,
        data: dict[str, t.Any],
    ) -> t.Any:
        services: ServicesStore = data['services_store']
        user = await services.user_service.get_or_none(t.cast(User, data['event_from_user']).id)
        data['user'] = user
        return await handler(event, data)
