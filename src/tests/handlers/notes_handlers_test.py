from unittest import mock

import pytest

from todolist.database.entities.user_entity import UserEntity
from todolist.handlers import notes_handlers as handlers

from .helpers import assert_state_endpoint, assert_register_handled

@pytest.mark.parametrize("user", (UserEntity(id=1, telegram_id=1, email='email', name='name'), None))
async def test_addnote_entrypoint(state: mock.Mock, answer_to: mock.Mock, user: UserEntity | None) -> None:
    await handlers.addnote_entrypoint_handler(None, answer_to, state, user)
    if user is None: return assert_register_handled(state, answer_to)
    assert_state_endpoint(state)
    answer_to.assert_called()
