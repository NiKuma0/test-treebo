from unittest import mock
import pytest

from todolist.services import ServicesStore
from todolist.services import UserService, NoteService
from todolist.utils import AnswerToAbc


class ServiceStoreMock(ServicesStore):
    def __init__(
        self,
    ) -> None:
        self.user_service = mock.MagicMock(UserService)
        self.note_service = mock.MagicMock(NoteService)


@pytest.fixture(name="state")
def get_state():
    return mock.AsyncMock()


@pytest.fixture(name="answer_to")
def get_answer_to_mock():
    return mock.AsyncMock(AnswerToAbc)


@pytest.fixture(name="services_store")
def get_services_store():
    return ServiceStoreMock()
