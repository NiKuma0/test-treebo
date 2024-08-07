from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User

from todolist.services import ServicesStore
from todolist.states import UserInputStates
from todolist.utils import AnswerToAbc

from .constants import MENU


router = Router()


async def register_handler(answer_to: AnswerToAbc, state: FSMContext):
    await answer_to("Send me your name:")
    await state.clear()
    await state.set_state(UserInputStates.name)


@router.message(UserInputStates.name)
async def set_name_handler(message: Message, state: FSMContext, answer_to: AnswerToAbc):
    if message.text is None:
        return
    await state.update_data(name=message.text)
    await answer_to("Send me your email:")
    await state.set_state(UserInputStates.email)


@router.message(UserInputStates.email)
async def set_email_handler(
    message: Message,
    state: FSMContext,
    answer_to: AnswerToAbc,
    services_store: ServicesStore,
    event_from_user: User,
):
    if message.text is None:
        return
    data = await state.get_data()
    await services_store.user_service.register(
        email=message.text, name=data["name"], telegram_id=event_from_user.id
    )
    await state.clear()
    await answer_to(
        "Registration done!\nGo to main menu -> /start",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Main menu", callback_data=MENU)]
            ]
        ),
    )
