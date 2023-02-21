import requests

from config import notify_url


def get_pay_url(order_id, amount, nominal):
    request = requests.post("https://securepay.tinkoff.ru/v2/Init", json={
        "TerminalKey": 1667828213399,
        "Amount": amount * 100,
        "OrderId": order_id,
        "Description": f"Подарочная карта на {nominal}.00 рублей",
        "NotificationURL": notify_url,
        "SuccessURL": "https://t.me/ApplePayCard_bot"
    })
    return request.json()["PaymentURL"]
