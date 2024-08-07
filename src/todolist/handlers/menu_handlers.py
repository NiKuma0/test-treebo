from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, Command

from todolist.database.entities.user_entity import UserEntity
from todolist.handlers.register_handler import register_handler
from todolist.utils import AnswerToAbc

from .constants import CREATE_TASK, MENU


router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == MENU)
async def start_handler(
    _, state: FSMContext, answer_to: AnswerToAbc, user: UserEntity | None
):
    if user is None:
        await register_handler(answer_to, state)
        return
    await state.clear()
    await answer_to(
        f"Hello, {user.name}!\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=CREATE_TASK)]]),
    )


@router.message(Command("cancel"))
async def cancel_handler(_: Message, answer_to: AnswerToAbc, state: FSMContext):
    await state.clear()
    await answer_to("Canceled! Come back to start menu -> /start.")
