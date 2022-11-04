from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeTierState(StatesGroup):
    user_id = State()


class ChangeUsernameState(StatesGroup):
    user_id = State()


class ChangeEventState(StatesGroup):
    event_id = State()
