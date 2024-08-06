import pytest
from unittest import mock

from aiogram import Bot

from todolist.settings import Settings
from todolist.database.repositories import UserRepository, NoteRepository


class RepoStoreMock:
    def __init__(self) -> None:
        self._user_repo = mock.MagicMock(UserRepository)
        self._note_repo = mock.MagicMock(NoteRepository)
    @property
    def user_repo(self): return self._user_repo
    @property
    def note_repo(self): return self._note_repo


@pytest.fixture(name="repo_store_mock")
def get_repo_store_mock(): return RepoStoreMock()


@pytest.fixture(name="bot_mock")
def get_bot_mock(): return mock.Mock(Bot)


@pytest.fixture(name='settings')
def get_settings(): return Settings(
    DEBUG=True,
    BOT_TOKEN="TestingBotToken",
)
