import logging

from aiogram import Bot, Dispatcher

from todolist.middlewares import register_middlewares
from todolist.database import get_engine, get_sessionmaker
from todolist.database.entities import BaseEntity
from todolist.database.repositories import RepositoriesStore
from todolist.handlers import setup_handlers
from todolist.services import ServicesStore
from todolist.settings import get_settings


logging.basicConfig(level=logging.DEBUG)

settings = get_settings()
bot = Bot(settings.BOT_TOKEN)
dispatcher = Dispatcher()


engine = get_engine()
sessionmaker = get_sessionmaker(engine)


@dispatcher.startup()
async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)


repo_store = RepositoriesStore(sessionmaker)
services_store = ServicesStore(repo_store, settings, bot)

register_middlewares(dispatcher, services_store)
setup_handlers(dispatcher)

dispatcher.run_polling(bot, services_store=services_store, settings=settings)  # type: ignore
