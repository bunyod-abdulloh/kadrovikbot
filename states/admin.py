from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    NO_TEXT = State()
    CHECK_NO_TEXT = State()
