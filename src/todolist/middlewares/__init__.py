from aiogram import Dispatcher

from todolist.services import ServicesStore

from .get_answer_to import AnswerToMiddleware
from .user_middleware import UserMiddleware


__all__ = (
    "AnswerToMiddleware",
    "UserMiddleware",
)


def register_middlewares(dispatcher: Dispatcher, services_store: ServicesStore):
    dispatcher.callback_query.middleware(AnswerToMiddleware())
    dispatcher.message.middleware(AnswerToMiddleware())
    dispatcher.callback_query.middleware(UserMiddleware())
    dispatcher.message.middleware(UserMiddleware())
