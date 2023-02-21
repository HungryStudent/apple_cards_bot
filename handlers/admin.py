from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from create_bot import dp
from config import manager_id
import keyboards.admin as admin_kb
import states.admin as states
from utils import db


@dp.callback_query_handler(Text(startswith="answer"), chat_id=manager_id)
async def enter_text(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    await call.message.answer("Введите ответ", reply_markup=admin_kb.cancel)
    await states.GiveCode.enter_text.set()
    await state.update_data(user_id=user_id, msg_id=call.message.message_id)
    await call.answer()


@dp.message_handler(state=states.GiveCode.enter_text, chat_id=manager_id)
async def give_code(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.bot.send_message(data["user_id"], message.text)
    await message.answer("Ответ отправлен пользователю", reply_markup=admin_kb.ReplyKeyboardRemove())
    await message.bot.edit_message_reply_markup(manager_id, data["msg_id"], reply_markup=None)
    await state.finish()


@dp.message_handler(chat_id=manager_id, commands="pricelist")
async def show_admin_pricelist(message: Message):
    await message.answer("Список карточек:", reply_markup=admin_kb.get_price_list())


@dp.callback_query_handler(chat_id=manager_id, text="create_price")
async def enter_nominal(call: CallbackQuery):
    await call.message.answer("Введите номинал", reply_markup=admin_kb.cancel)
    await states.CreatePrice.nominal.set()
    await call.answer()


@dp.message_handler(chat_id=manager_id, state=states.CreatePrice.nominal)
async def enter_amount(message: Message, state: FSMContext):
    await state.update_data(nominal=message.text.lower())
    await message.answer("Введите цену карточки")
    await states.CreatePrice.next()


@dp.message_handler(chat_id=manager_id, state=states.CreatePrice.amount)
async def enter_photo(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await message.answer("Пришлите фото карточки")
    await states.CreatePrice.next()


@dp.message_handler(content_types="photo", state=states.CreatePrice.photo)
async def create_price(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    price = await state.get_data()
    db.create_price(price)
    await message.answer("Карточка успешно создана", reply_markup=admin_kb.get_price_list())
    await state.finish()


@dp.callback_query_handler(Text(startswith="admin_price"))
async def show_admin_price(call: CallbackQuery):
    price = db.get_price(int(call.data.split(":")[1]))
    await call.message.answer_photo(price["photo"], caption=f"""Карта номиналом {price['nominal']}
На сумму {price['amount']}""", reply_markup=admin_kb.get_price(int(call.data.split(":")[1])))


@dp.callback_query_handler(Text(startswith="change"))
async def start_change(call: CallbackQuery, state: FSMContext):
    price_id = int(call.data.split(":")[2])
    key = call.data.split(":")[1]
    if key == "nominal":
        await states.ChangePrice.nominal.set()
        await call.message.answer("Введите новый номинал", reply_markup=admin_kb.cancel)
    elif key == "amount":
        await states.ChangePrice.amount.set()
        await call.message.answer("Введите новую цену", reply_markup=admin_kb.cancel)
    elif key == "photo":
        await states.ChangePrice.photo.set()
        await call.message.answer("Пришлите новое фото", reply_markup=admin_kb.cancel)
    await state.update_data(price_id=price_id)
    await call.answer()


@dp.message_handler(state=states.ChangePrice.nominal)
async def change_nominal(message: Message, state: FSMContext):
    try:
        nominal = int(message.text)
    except ValueError:
        await message.answer("Введите целое число!")
        return
    price = await state.get_data()
    db.change_price(price["price_id"], "nominal", nominal)
    await message.answer("Номинал изменен", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state=states.ChangePrice.amount)
async def change_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Введите целое число!")
        return
    price = await state.get_data()
    db.change_price(price["price_id"], "amount", amount)
    await message.answer("Цена изменена", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state=states.ChangePrice.photo, content_types="photo")
async def change_photo(message: Message, state: FSMContext):
    price = await state.get_data()
    db.change_price(price["price_id"], "photo", message.photo[-1].file_id)
    await message.answer("Фото изменено", reply_markup=admin_kb.ReplyKeyboardRemove())
    await state.finish()


@dp.callback_query_handler(Text(startswith="delete_price"))
async def delete_price(call: CallbackQuery):
    price_id = call.data.split(":")[1]
    await call.message.edit_caption("Вы действительно хотите удалить карточку?",
                                    reply_markup=admin_kb.get_delete(price_id))


@dp.callback_query_handler(Text(startswith="sure_delete"))
async def sure_delete_price(call: CallbackQuery):
    action = call.data.split(":")[1]
    price_id = call.data.split(":")[2]
    if action == "approve":
        db.delete_price(price_id)
        await call.message.answer("Карточка удалена", reply_markup=admin_kb.get_price_list())
        await call.message.delete()
    else:
        await call.message.answer("Список карточек", reply_markup=admin_kb.get_price_list())
        await call.message.delete()
