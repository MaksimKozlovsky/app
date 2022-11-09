from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    user = State()
    tier = State()
    username = State()
    password = State()


class ChangeUsernameState(StatesGroup):
    user_id = State()


class EventState(StatesGroup):
    event = State()
    ticket = State()
    date_st = State()

