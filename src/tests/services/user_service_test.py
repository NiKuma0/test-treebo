import pytest
from unittest import mock

from todolist.services import UserService
from todolist.settings import Settings
from todolist.database.entities import UserEntity

from .conftest import RepoStoreMock


@pytest.fixture(name="user_service")
def get_user_service(settings: Settings, bot_mock: mock.Mock, repo_store_mock: RepoStoreMock):
    return UserService(
        repo_store=repo_store_mock,
        settings=settings,
        bot=bot_mock
    )


async def test_user_register(user_service: UserService, repo_store_mock: RepoStoreMock):
    user_from_db = UserEntity(id=1, telegram_id=1, name="NoneName", email="email")
    repo_store_mock.user_repo.get_or_create.return_value = user_from_db

    user_from_service = await user_service.register(
        name="Another Name",
        email="Another email",
        telegram_id=2,
    )
    repo_store_mock.user_repo.get_or_create.assert_called_once()
    assert user_from_service is user_from_db


@pytest.mark.parametrize("user_from_db", [
    (UserEntity(id=1, telegram_id=1, name="NoneName", email="email"),),
    (None,)
])
async def test_user_service_get_or_none(user_from_db: UserEntity | None, user_service: UserService, repo_store_mock: RepoStoreMock):
    repo_store_mock.user_repo.get_by_telegram_id.return_value = user_from_db
    user_from_service = await user_service.get_or_none(telegram_id=2)
    repo_store_mock.user_repo.get_by_telegram_id.assert_called_once()
    assert user_from_service is user_from_db
