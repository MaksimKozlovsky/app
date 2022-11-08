import logging
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from app.services.event_playground import event_service
from app.services.tier_state import UserState, ChangeUsernameState, EventState
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.json_to_text import convert_to_text, convert_to_text_ticket

load_dotenv()

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
GLOBAL_DATA: dict = {}
NOT_FOUND_TIER = "NOT_FOUND"


async def startup(_):
    event_service.check_availability()
    GLOBAL_DATA["tiers"] = event_service.get_tiers()
    GLOBAL_DATA["tiers"].update({"Deactivate tier": None})


@dp.message_handler(commands=["admin"])
async def get_admin_commands(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Get users", callback_data="get_users_1"))
    inline_kb.add(types.InlineKeyboardButton("Get events", callback_data="get_events_1"))
    await msg.reply("Choose admin action", reply_markup=inline_kb)


@dp.callback_query_handler(Text(contains="get_users"))
async def display_users(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    users_response = event_service.get_users(page)

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
    await callback.answer("Users fetched")


@dp.callback_query_handler(Text(contains="get_user"))
async def display_user(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[-1])
    user = event_service.get_user(user_id)

    await state.set_state(UserState.user.state)
    await state.update_data(user, msg_id=callback.message.message_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Change tier", callback_data="change_tier"))
    inline_kb.add(types.InlineKeyboardButton("Change username", callback_data="change_username"))
    inline_kb.add(types.InlineKeyboardButton("Change password", callback_data="change_password"))

    msg_text = convert_to_text(user)

    await callback.message.edit_text(msg_text, reply_markup=inline_kb)
    await callback.answer("User fetched")


@dp.callback_query_handler(Text(equals="change_tier"), state=UserState.user)
async def choose_tier(callback: types.CallbackQuery, state: FSMContext):
    inline_kb = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)

    for human_tier in GLOBAL_DATA["tiers"]:
        inline_kb.add(types.KeyboardButton(human_tier))

    await state.set_state(UserState.tier.state)
    msg = await callback.message.answer("Choose Tier", reply_markup=inline_kb)
    await state.update_data(msg_to_delete=msg.message_id, msg_id=callback.message.message_id)


@dp.message_handler(state=UserState.tier)
async def change_tier(msg: types.Message, state: FSMContext):
    new_tier = GLOBAL_DATA["tiers"].get(msg.text, NOT_FOUND_TIER)

    if new_tier == NOT_FOUND_TIER:
        await msg.reply("Choose normal tier")
        return

    data = await state.get_data()
    user = event_service.update_user(data["id"], {"tier": new_tier})

    msg_text = convert_to_text(user)

    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"])
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()


@dp.callback_query_handler(Text(equals="change_username"), state=UserState.user)
async def username_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.username.state)
    msg = await callback.message.answer("Type new username")
    await state.update_data(msg_to_delete=msg.message_id, msg_id=callback.message.message_id)


@dp.message_handler(state=UserState.username)
async def change_username(msg: types.Message, state: FSMContext):
    username = msg.text.strip()
    data = await state.get_data()
    user = event_service.update_user(data["id"], {"username": username})
    msg_text = convert_to_text(user)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"])
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()

# # ----------------------------------------------------------------------------------------------------------


@dp.callback_query_handler(Text(equals="change_password"), state=UserState.user)
async def password_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.password.state)
    msg = await callback.message.answer("Type new password")
    await state.update_data(msg_to_delete=msg.message_id, msg_id=callback.message.message_id)


@dp.message_handler(state=UserState.password)
async def change_password(msg: types.Message, state: FSMContext):
    password = msg.text.strip()
    data = await state.get_data()
    user = event_service.update_password(data["id"], {"password": password})
    msg_text = convert_to_text(user)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"])
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()

# # ------------------------------ EVENTS ----------------------------------------------------------------------------


@dp.callback_query_handler(Text(contains="get_events"))
async def display_events(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    events_response = event_service.get_events(page)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    for event in events_response["results"]:
        inline_kb.add(
            types.InlineKeyboardButton(f"id: {event['id']}.\n"
                                       f"Название: {event['title']}.\n"
                                       f"Дата: {event['date']}",
                                       callback_data=f"get_event:{event['id']}")
        )

    pagination_buttons = []

    if events_response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("previous", callback_data=f"get_events_{page - 1}"))
    if events_response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("next", callback_data=f"get_events_{page + 1}"))

    await callback.message.edit_text("Edited", reply_markup=inline_kb.row(*pagination_buttons))


@dp.callback_query_handler(Text(contains="get_event"))
async def display_event(callback: types.CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split(":")[-1])
    event = event_service.get_event(event_id)

    await state.set_state(EventState.event.state)
    await state.update_data(event, msg_id=callback.message.message_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Change ticket count", callback_data="change_ticket_count"))
    inline_kb.add(types.InlineKeyboardButton("Change date", callback_data="change_date"))

    msg_text = convert_to_text(event)

    await callback.message.edit_text(msg_text, reply_markup=inline_kb)
    await callback.answer("Event fetched")


@dp.callback_query_handler(Text(equals="change_ticket_count"), state=EventState.event)
async def ticket_change_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EventState.ticket.state)
    msg = await callback.message.answer("Type new ticket count")
    await state.update_data(msg_to_delete=msg.message_id, msg_id=callback.message.message_id)


@dp.message_handler(state=EventState.ticket)
async def change_ticket_count(msg: types.Message, state: FSMContext):
    ticket_count = msg.text.strip()
    data = await state.get_data()
    ticket = event_service.update_ticket_count(data["id"], {"ticket_count": ticket_count})
    msg_text = convert_to_text_ticket(ticket)
    await bot.edit_message_text(msg_text, msg.chat.id, data["msg_id"])
    await bot.delete_message(msg.chat.id, data["msg_to_delete"])
    await msg.delete()
    await state.finish()

# # ------------------ END EVENTS -------------------------------------------------------------------------------------

executor.start_polling(dp, skip_updates=True, on_startup=startup)
