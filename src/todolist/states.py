from aiogram.fsm.state import StatesGroup, State


class UserInputStates(StatesGroup):
    name = State()
    email = State()

    note_text = State()
    note_datetime = State()
