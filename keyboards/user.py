from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from utils import db

from utils.pay import get_pay_url

select_prompt_callback = CallbackData("select_prompt", "prompt_id")

menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Выбрать номинал карты", callback_data="show_price_list"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))


def get_price_list():
    kb = InlineKeyboardMarkup(row_width=1)
    price_list = db.get_price_list()
    for price in price_list:
        kb.add(InlineKeyboardButton(price["nominal"], callback_data=f"buy:{price['id']}"))
    return kb


def get_pay(user_id, price_id):
    order_id = db.create_order(user_id, price_id)
    price = db.get_price(price_id)
    pay_url = get_pay_url(order_id, price["amount"], price["nominal"])
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(f"Оплатить", url=pay_url),
        InlineKeyboardButton(f"*УСЛОВНО ОПЛАТИЛ*", callback_data=f"success:{price_id}"))
