from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
import keyboards.admin as admin_kb
import keyboards.user as user_kb

from config import ADMINS, price_list, manager_id
from create_bot import dp
from utils import db


@dp.message_handler(content_types="photo")
async def show_file_id(message: Message):
    await message.answer(message.photo[-1].file_id)


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: Message, state: FSMContext):
    await state.finish()

    user = db.get_user(message.from_user.id)
    if user is None:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer("Привет, я эплкарта бот, созданный для покупки подарочных карт, бла бла бла",
                         reply_markup=user_kb.menu)


@dp.message_handler(state="*", text="Отмена")
async def cancel(message: Message):
    await message.answer("Ввод отменен", reply_markup=user_kb.ReplyKeyboardRemove())


@dp.callback_query_handler(text="show_price_list")
async def show_price_list(call: CallbackQuery):
    await call.message.edit_text("Какой номинал карты вы хотите приобрести?", reply_markup=user_kb.get_price_list())


@dp.callback_query_handler(Text(startswith="buy"))
async def show_price(call: CallbackQuery):
    price_id = int(call.data.split(":")[1])
    price = db.get_price(price_id)
    await call.message.answer_photo(price["photo"],
                                    caption=f"Окей, с учетом комисcии сервиса к оплате будет {price['amount']}, "
                                            f"после оплаты код придет вам в этот чат в течении 15 минут",
                                    reply_markup=user_kb.get_pay(call.from_user.id, price_id))
