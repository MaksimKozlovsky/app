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
    n_event = State()


# class Form(StatesGroup):
#     name = State()  # Will be represented in storage as 'Form:name'
#     age = State()  # Will be represented in storage as 'Form:age'
#     gender = State()  # Will be represented in storage as 'Form:gender'