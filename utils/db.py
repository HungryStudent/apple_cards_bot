from contextlib import closing
from datetime import datetime
from sqlite3 import Cursor
import sqlite3

database = "utils/database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, first_name TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, price_id INT, is_paid BOOL, create_time INT, pay_time INT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS price_list(id INTEGER PRIMARY KEY AUTOINCREMENT, nominal INT, amount INT, photo TEXT)")
        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def add_user(user_id, username, first_name):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, username, first_name))
        connection.commit()


def create_order(user_id, price_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO orders(user_id, price_id, is_paid, create_time) VALUES (?, ?, FALSE, ?)",
                       (user_id, price_id, int(datetime.now().timestamp())))
        order_id = cursor.lastrowid
        connection.commit()
        return order_id


def get_order(order_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(
            "SELECT orders.user_id, price_id, is_paid, u.username FROM orders JOIN users u on orders.user_id = u.user_id WHERE id = ?",
            (order_id,))
        return cursor.fetchone()


def change_order_status(order_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("UPDATE orders SET is_paid = TRUE, pay_time = ? WHERE id = ?",
                       (int(datetime.now().timestamp()), order_id,))
        connection.commit()


def get_price_list():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT * FROM price_list")
        return cursor.fetchall()


def create_price(price):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO price_list(nominal, amount, photo) VALUES (?, ?, ?)",
                       (price["nominal"], price["amount"], price["photo"]))
        connection.commit()


def delete_price(price_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("DELETE FROM price_list WHERE id = ?", (price_id,))
        connection.commit()


def get_price(price_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT * FROM price_list WHERE id = ?", (price_id,))
        return cursor.fetchone()


def change_price(price_id, key, value):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(f"UPDATE price_list SET {key} = ? WHERE id = ?",
                       (value, price_id))
        connection.commit()
