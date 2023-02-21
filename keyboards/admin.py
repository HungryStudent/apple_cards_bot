from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from utils import db

prompt_callback = CallbackData("rule", "id")
delete_prompt_callback = CallbackData("sure_delete", "action", "id")

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))


def get_give_code(user_id):
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Ответить", callback_data=f"answer:{user_id}"))


def get_price_list():
    price_list = db.get_price_list()
    kb = InlineKeyboardMarkup(row_width=1)
    for price in price_list:
        kb.add(
            InlineKeyboardButton(f"{price['nominal']} - {price['amount']}", callback_data=f"admin_price:{price['id']}"))
    kb.add(InlineKeyboardButton("Добавить", callback_data="create_price"))
    return kb


def get_price(price_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Изменить номинал", callback_data=f"change:nominal:{price_id}"),
        InlineKeyboardButton("Изменить цену", callback_data=f"change:amount:{price_id}"),
        InlineKeyboardButton("Изменить фото", callback_data=f"change:photo:{price_id}"),
        InlineKeyboardButton("Удалить карточку", callback_data=f"delete_price:{price_id}"))


def get_delete(price_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Да, удалить", callback_data=f"sure_delete:approve:{price_id}"),
        InlineKeyboardButton("Нет, не удалять", callback_data=f"sure_delete:cancel:{price_id}"))
