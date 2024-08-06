import asyncio
from http import HTTPStatus
import typing as t
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from pydantic import ValidationError

from todolist.clients import AsyncScheduledNotification
from todolist.middlewares import register_middlewares
from todolist.database import get_engine, get_sessionmaker
from todolist.database.repositories import RepositoriesStore
from todolist.handlers import setup_handlers
from todolist.services import ServicesStore
from todolist.settings import get_settings

if t.TYPE_CHECKING:
    from aws_lambda_typing import context, events, responses


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

loop = asyncio.get_event_loop()
settings = get_settings()
logger.info("Init")
bot = Bot(settings.BOT_TOKEN)
dispatcher = Dispatcher()

engine = get_engine()
sessionmaker = get_sessionmaker(engine)

repo_store = RepositoriesStore(sessionmaker)
services_store = ServicesStore(repo_store, settings, bot, schedule_client=AsyncScheduledNotification(bot))

register_middlewares(dispatcher, services_store)
setup_handlers(dispatcher)

def handler(event: 'events.APIGatewayProxyEventV2', context: 'context.Context') -> 'responses.APIGatewayProxyResponseV2':
    logger.info("Starting validation")
    try:
        update = Update.model_validate_json(event.get('body', ''), strict=False)
    except ValidationError as e:
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': e.json()
        }

    logger.info("Feeding update to dispatcher.")
    loop.run_until_complete(
        dispatcher.feed_update(
            bot, update=update, services_store=services_store, settings=settings,
        )
    )
    logger.info("Returning status code.")
    return { 'statusCode': HTTPStatus.OK }
