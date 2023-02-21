import uvicorn as uvicorn
from fastapi import FastAPI, Request

from keyboards import admin as admin_kb
from config import manager_id
from utils import db
from create_bot import bot

app = FastAPI()


@app.post('/api/pay')
async def check_pay(req: Request):
    data = await req.json()
    if data["Status"] == "CONFIRMED":
        order_id = int(data["OrderId"])
        db.change_order_status(order_id)
        order = db.get_order(order_id)
        if order is None:
            return "OK"
        price = db.get_price(order["price_id"])
        await bot.send_message(order["user_id"],
                               "Ваша карта оплачена и придет в этот чат в течении 15 минут, если что, ответим на все вопросы прям в этом чате, хорошего дня)")
        await bot.send_message(manager_id, f"""Новая заявка на карту:
Пользователь: @{order["username"]}
Карта номиналом {price['nominal']}
На сумму {price['amount']}""", reply_markup=admin_kb.get_give_code(order["user_id"]))
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
