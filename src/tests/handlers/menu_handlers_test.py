from unittest import mock

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import pytest

from todolist.handlers.constants import CREATE_TASK
from todolist.database.entities.user_entity import UserEntity
from todolist.handlers.menu_handlers import start_handler, cancel_handler

from .helpers import assert_register_handled, assert_state_endpoint


@pytest.mark.parametrize(
    "user", [None, UserEntity(id=1, telegram_id=1, email="email", name="name")]
)
async def test_menu_handler(
    state: mock.Mock, answer_to: mock.Mock, user: UserEntity | None
):
    await start_handler(None, state, answer_to, user)
    if user is None:
        return assert_register_handled(state, answer_to)

    assert_state_endpoint(state)
    answer_to.assert_called_with(
        f"Hello, {user.name}!\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=CREATE_TASK)]]),
    )


async def test_cancel_handler(state: mock.Mock, answer_to: mock.Mock):
    await cancel_handler(None, answer_to, state)
    assert_state_endpoint(state)
    answer_to.assert_called_once()
