from aiogram.dispatcher.filters.state import StatesGroup, State


class GiveCode(StatesGroup):
    enter_text = State()


class CreatePrice(StatesGroup):
    nominal = State()
    amount = State()
    photo = State()


class ChangePrice(StatesGroup):
    nominal = State()
    amount = State()
    photo = State()