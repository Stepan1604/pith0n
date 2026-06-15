from aiogram import types

from Sample.Bot.vars.dialog import HELLO_TEXT, GOODBYE_TEXT


def get_kb():
    kb = [
        [
            types.KeyboardButton(text="Привет"),
            types.KeyboardButton(text="Пока")
        ],
        [
            types.KeyboardButton(text=HELLO_TEXT),
            types.KeyboardButton(text=GOODBYE_TEXT)
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                         resize_keyboard=True,
                                         input_field_placeholder=""
                                         )
    return keyboard