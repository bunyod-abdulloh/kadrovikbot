from aiogram.dispatcher.filters.state import StatesGroup, State


class AnketaStates(StatesGroup):
    FULLNAME = State()
    BIRTHDATE = State()
    EDUCATION = State()
    SPECIALTY = State()
    REGION = State()
    DISTRICT = State()
    PHONE = State()
    CHECK = State()
