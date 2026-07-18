from aiogram import types
from Bot.vars.dialog import HELLO_TEXT, GOODBYE_TEXT


def get_kb():
    """Create main keyboard with buttons"""
    kb = [
        [
            types.KeyboardButton(text="Привет"),
            types.KeyboardButton(text="Пока")
        ],
        [
            types.KeyboardButton(text=HELLO_TEXT),
            types.KeyboardButton(text=GOODBYE_TEXT)
        ],
        [
            types.KeyboardButton(text="📋 Новый план питания"),
            types.KeyboardButton(text="📊 Мой профиль")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard


def get_goal_kb():
    """Keyboard for selecting nutrition goal"""
    kb = [
        [types.KeyboardButton(text="💪 Похудеть")],
        [types.KeyboardButton(text="🏋️ Поддерживать форму")],
        [types.KeyboardButton(text="🥗 Сбалансированное питание")],
        [types.KeyboardButton(text="👨‍👩‍👧‍👦 Меню для семьи")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_duration_kb():
    """Keyboard for selecting meal plan duration"""
    kb = [
        [types.KeyboardButton(text="📅 На неделю")],
        [types.KeyboardButton(text="📆 На месяц")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_yes_no_kb():
    """Yes/No keyboard"""
    kb = [
        [types.KeyboardButton(text="✅ Да"), types.KeyboardButton(text="❌ Нет")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
