import datetime as dt
import pytest
from unittest import mock

from todolist.services import NoteService
from todolist.settings import Settings
from todolist.database.entities import NoteEntity
from todolist.clients import ScheduledNotificationAbc

from .conftest import RepoStoreMock


@pytest.fixture(name="schedule_client")
def get_schedule_client(): return mock.Mock(ScheduledNotificationAbc)

@pytest.fixture(name="note_service")
def get_note_service(settings: Settings, bot_mock: mock.Mock, repo_store_mock: RepoStoreMock, schedule_client: mock.Mock):
    return NoteService(
        repo_store=repo_store_mock,
        settings=settings,
        bot=bot_mock,
        schedule_client=schedule_client,
    )


async def test_service(note_service: NoteService, repo_store_mock: RepoStoreMock, schedule_client: mock.Mock):
    remainder_time = dt.datetime.now()
    note_from_db = NoteEntity(text="Text", remainder_time=remainder_time)
    repo_store_mock.note_repo.create.return_value = note_from_db
    note_from_service = await note_service.create(
        chat_id=1,
        remainder_time=remainder_time,
        text="text",
        user_id=1,
    )
    schedule_client.send_message.assert_called_once_with(
        remainder_time, chat_id=1, text="text",
    )
    repo_store_mock.note_repo.create.assert_called_once()
    assert note_from_db is note_from_service
