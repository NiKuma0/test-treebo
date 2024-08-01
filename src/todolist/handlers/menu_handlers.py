from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from aiogram.filters import CommandStart, Command

from todolist.utils import to_html_str


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, event_from_user: User, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {to_html_str(event_from_user.full_name)}\n"
    )


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено! Вернуться на старт -> /start.')
