import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.enums.update_type import UpdateType

from todolist.clients import AsyncScheduledNotification
from todolist.middlewares import register_middlewares
from todolist.database import get_engine, get_sessionmaker
from todolist.database.entities import BaseEntity
from todolist.database.repositories import RepositoriesStore
from todolist.handlers import setup_handlers
from todolist.services import ServicesStore
from todolist.settings import get_settings


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('aiosqlite').disabled = True

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
services_store = ServicesStore(repo_store, settings, bot, schedule_client=AsyncScheduledNotification(bot))

register_middlewares(dispatcher, services_store)
setup_handlers(dispatcher)

if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(
            dispatcher.start_polling(bot, allowed_updates=[UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY], services_store=services_store, settings=settings),  # type: ignore
            debug=settings.DEBUG,
        )
