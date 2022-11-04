import logging
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from app.services.event_playground import user_service, event_service
from app.services.tier_state import ChangeTierState, ChangeUsernameState, ChangeEventState
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
TIERS = ['Gold', 'Silver', 'Platinum', 'Deactivate tier']
USERNAMES = ['OO', 'OO-O', 'OOO', 'OOOO']


async def startup(_):
    response = requests.get("http://127.0.0.1:8000/ping/")
    response.raise_for_status()
#    await message.reply(f'Status: {response.raise_for_status()}')
#
#
# @dp.message_handler(commands=["admin"])
# async def get_admin_commands(msg: types.Message):
#     inline_kb = types.InlineKeyboardMarkup(row_width=1)
#     inline_kb.add(types.InlineKeyboardButton("Get users", callback_data="get_users_1"))
#     inline_kb.add(types.InlineKeyboardButton("Get events", callback_data="events_1"))
#     await msg.reply("Choose admin action", reply_markup=inline_kb)
#
# # --------------------------------------------------------------------------------------------
#
#
# @dp.callback_query_handler(Text(contains='user_id:'))
# async def get_user(callback: types.CallbackQuery):
#     user_id = int(callback.data.split(":")[-1])
#     user = user_service.get_user(user_id)
#     print(user)
#     inline = types.InlineKeyboardMarkup(row_width=1)
#     inline.add(types.InlineKeyboardButton(f"id: {user['id']}. \n"
#                                           f"tier: {user['tier']}. \n"
#                                           f"username: {user['username']}. \n"
#                                           f"{user['email']}",
#                                           callback_data='get_user:')
#                )
#     inline.add(types.InlineKeyboardButton('modify tier', callback_data='tier'))
#
#     await callback.message.reply('user', reply_markup=inline)
#
#
# @dp.callback_query_handler((Text(contains='tier')))
# async def get_kb(callback: types.CallbackQuery):
#     k_b = [
#         [types.KeyboardButton(text='SILVER')],
#         [types.KeyboardButton(text='GOLD')],
#         [types.KeyboardButton(text='PLATINUM')]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=k_b, row_width=1, resize_keyboard=True)
#     await callback.message.reply('your choice', reply_markup=keyboard)
#
#
# # ---------------------------------------------------------------------------------------
#
# @dp.callback_query_handler(Text(contains="get_users"))
# async def display_users(callback: types.CallbackQuery):
#     page = int(callback.data.split("_")[-1])
#     users_response = user_service.get_users(page)
#
#     inline_kb = types.InlineKeyboardMarkup(row_width=1)
#
#     for user in users_response["results"]:
#         inline_kb.add(
#             types.InlineKeyboardButton(f"{user['id']}. {user['username']}", callback_data=f"user_id:{user['id']}")
#         )
#
#     pagination_buttons = []
#
#     if users_response["previous"]:
#         pagination_buttons.append(types.InlineKeyboardButton("⬅️👹😈", callback_data=f"get_users_{page - 1}"))
#     if users_response["next"]:
#         pagination_buttons.append(types.InlineKeyboardButton("👹😈➡️", callback_data=f"get_users_{page + 1}"))
#
#     await callback.message.edit_text("Edited", reply_markup=inline_kb.row(*pagination_buttons))
#
# # ---------------------------------------------------------------------------------------------------------------------
#
#
# @dp.callback_query_handler(Text(contains="events"))
# async def display_events(callback: types.CallbackQuery):
#     page = int(callback.data.split("_")[-1])
#     events_response = event_service.get_events(page)
#
#     inline_kb = types.InlineKeyboardMarkup(row_width=1)
#
#     for event in events_response["results"]:
#         inline_kb.add(
#             types.InlineKeyboardButton(f"id: {event['id']}.\n"
#                                        f"Название: {event['title']}.\n"
#                                        f"Описание: {event['description']}",
#                                        callback_data=f"vent_id:{event['id']}")
#         )
#
# #    import textwrap
# #    InlineKeyboardButton(textwrap.fill(answer)
#     pagination_buttons = []
#
#     if events_response["previous"]:
#         pagination_buttons.append(types.InlineKeyboardButton("previous", callback_data=f"get_events_{page - 1}"))
#     if events_response["next"]:
#         pagination_buttons.append(types.InlineKeyboardButton("next", callback_data=f"get_events_{page + 1}"))
#
#     await callback.message.edit_text("Edited", reply_markup=inline_kb.row(*pagination_buttons))
#
# # -------------------------------------------------------------------------------------------------------------------
#
# executor.start_polling(dp, skip_updates=True, on_startup=startup)


@dp.message_handler(commands=["admin"])
async def get_admin_commands(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Get users", callback_data="get_users_1"))
    inline_kb.add(types.InlineKeyboardButton("Get events", callback_data="events_1"))
    await msg.reply("Choose admin action", reply_markup=inline_kb)


@dp.callback_query_handler(Text(contains="get_users"))
async def display_users(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    users_response = user_service.get_users(page)
    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    for user in users_response["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"{user['id']}. {user['username']}", callback_data=f"get_user:{user['id']}")
        )

    pagination_buttons = []

    if users_response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"get_users_{page - 1}"))
    if users_response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"get_users_{page + 1}"))

    await callback.message.edit_text("Edited", reply_markup=inline_kb.row(*pagination_buttons))
#    await callback.answer("Users fetched")


@dp.callback_query_handler(Text(contains="get_user"))
async def display_user(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[-1])
    user = user_service.get_user(user_id)

    await state.set_state(ChangeTierState.user_id.state)
#    await state.set_state(ChangeUsernameState.user_id.state)
    await state.update_data(user)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Change tier", callback_data="change_tier"))
    inline_kb.add(types.InlineKeyboardButton("Change username", callback_data="change_username"))

    user_html = ""
    for field, value in user.items():
        user_html += f"{field.capitalize()}: {value}\n"

    await callback.message.edit_text(user_html, reply_markup=inline_kb, parse_mode="HTML")
#    await callback.answer("User fetched")


@dp.callback_query_handler(Text(equals="change_tier"), state=ChangeTierState.user_id)
async def choose_tier(callback: types.CallbackQuery):
    inline_kb = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)

    for tier in TIERS:
        inline_kb.add(types.KeyboardButton(tier))

    await callback.message.answer("Choose Tier", reply_markup=inline_kb)


@dp.callback_query_handler(Text(equals='change_username'), state=ChangeTierState.user_id)
async def choose_username(callback: types.CallbackQuery):
    inline_kb = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)

    for username in USERNAMES:
        inline_kb.add(types.KeyboardButton(username))

    await callback.message.answer('Choose username', reply_markup=inline_kb)


@dp.message_handler(state=ChangeTierState.user_id)
async def set_state(msg: types.Message, state: FSMContext):
    new_tier = msg.text[0]
    data = await state.get_data()
    user = user_service.update_user(data["id"], {"tier": new_tier})
#    user = user_service.get_user(user_id)
    await msg.delete()
    await state.finish()


@dp.message_handler(state=ChangeTierState.user_id)
async def sett_state(msg: types.Message, state: FSMContext):
    new_username = msg.text[0]
    data = await state.get_data()
    user = user_service.update_user(data['id'], {'username': new_username})
    await msg.delete()
    await state.finish()

# # -------------------------- EVENTS ---------------------------------------------------------------------------------


@dp.callback_query_handler(Text(contains="events"))
async def display_events(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    events_response = event_service.get_events(page)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    for event in events_response["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"id: {event['id']}.\n"
                                       f"Название: {event['title']}.\n"
                                       f"Дата: {event['date']}",
                                       callback_data=f"event_id:{event['id']}")
        )

    pagination_buttons = []

    if events_response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("previous", callback_data=f"get_events_{page - 1}"))
    if events_response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("next", callback_data=f"get_events_{page + 1}"))

    await callback.message.edit_text("Edited", reply_markup=inline_kb.row(*pagination_buttons))


@dp.callback_query_handler(Text(contains="event_id"))
async def display_event(callback: types.CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split("_")[-1])
    event = event_service.get_event(event_id)

    await state.set_state(ChangeEventState.event_id.state)
    await state.update_data(event)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Change title", callback_data="change_title"))
    inline_kb.add(types.InlineKeyboardButton("Change date", callback_data="date"))

    event_html = ""
    for field, value in event.items():
        event_html += f"{field.capitalize()}: {value}\n"

    await callback.message.edit_text(event_html, reply_markup=inline_kb, parse_mode="HTML")
    await callback.answer("Event fetched")
# # -------------------------------------------------------------------------------------------------------------------

executor.start_polling(dp, skip_updates=True, on_startup=startup)
