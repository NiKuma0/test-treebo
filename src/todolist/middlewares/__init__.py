from aiogram import Dispatcher

from todolist.services import ServicesStore

from .user_register import UserRegisterMiddleware
from .get_answer_to import AnswerToMiddleware


__all__ = (
    "UserRegisterMiddleware",
    "AnswerToMiddleware",
)


def register_middlewares(dispatcher: Dispatcher, services_store: ServicesStore):
    dispatcher.callback_query.middleware(AnswerToMiddleware())
    dispatcher.message.middleware(AnswerToMiddleware())
