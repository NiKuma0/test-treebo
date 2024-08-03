import datetime
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from todolist.clients.exceptions import BackToTheFuture
from todolist.database.entities.note_entity import NoteEntity
from todolist.database.entities.user_entity import UserEntity
from todolist.handlers.register_handler import register_handler
from todolist.services import ServicesStore
from todolist.states import UserInputStates
from todolist.utils import AnswerToAbc

from .constants import CREATE_TASK, DATETIME_FORMAT


router = Router()
logger = logging.getLogger(__name__)

def note_to_str(note: NoteEntity):
    return (
        f"#{note.id}\n"
        f"{note.text}\n"
        f"Remainder time: {note.remainder_time.strftime("%d/%m %H:%M")}"
    )


@router.message(F.text == CREATE_TASK)
@router.message(Command("addnote"))
async def addnote_entrypoint_handler(_: Message, answer_to: AnswerToAbc, state: FSMContext, user: UserEntity | None):
    if user is None:
        await register_handler(answer_to, state)
        return
    await state.clear()
    await state.set_state(UserInputStates.note_text)
    await answer_to(
        "Send me text of the note:"
    )


@router.message(UserInputStates.note_text)
async def set_note_text(message: Message, answer_to: AnswerToAbc, state: FSMContext):
    if message.text is None: return
    await state.update_data(note_text=message.text)
    await state.set_state(UserInputStates.note_datetime)
    await answer_to(f"Send date and time in format {datetime.datetime.now().strftime(DATETIME_FORMAT)}")


@router.message(UserInputStates.note_datetime)
async def addnote_endpoint_handler(message: Message, answer_to: AnswerToAbc, state: FSMContext, services_store: ServicesStore, user: UserEntity | None):
    if message.text is None: return
    if user is None: return
    try:
        remainder_time = datetime.datetime.strptime(message.text, DATETIME_FORMAT)
    except ValueError:
        await answer_to(f"Can't parse date and time - value ({message.text}) doesn't match format.")
        return
    data = await state.get_data()
    try:
        await services_store.note_service.create(
            chat_id=message.chat.id,
            user_id=user.id,
            text=data['note_text'],
            remainder_time=remainder_time,
        )
    except BackToTheFuture:
        await answer_to("Notifications into the past are not possible. Timezone should be ")
        return
    except Exception as e:
        await answer_to("Something went wrong. Try again later.\nGo to start menu -> /start")
        raise e
    finally:
        await state.clear()

    await answer_to("Done!")



@router.message(Command('mynotes'))
async def get_my_notes(_: Message, answer_to: AnswerToAbc, services_store: ServicesStore, user: UserEntity | None):
    if user is None: return
    notes = await services_store.note_service.get_my_notes(user.id)
    await answer_to(
        '\n-----\n'.join([note_to_str(note) for note in notes])
    )
