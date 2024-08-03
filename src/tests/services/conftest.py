import pytest
from unittest import mock

from aiogram import Bot

from todolist.database.repositories import RepositoriesStore
from todolist.settings import Settings
from todolist.database.repositories import UserRepository, NoteRepository


class RepoStoreMock(RepositoriesStore):
    def __init__(self) -> None:
        self.user_repo = mock.MagicMock(UserRepository)
        self.note_repo = mock.MagicMock(NoteRepository)


@pytest.fixture(name="repo_store_mock")
def get_repo_store_mock(): return RepoStoreMock()


@pytest.fixture(name="bot_mock")
def get_bot_mock(): return mock.Mock(Bot)


@pytest.fixture(name='settings')
def get_settings(): return Settings(
    DEBUG=True,
    BOT_TOKEN="TestingBotToken",
)
