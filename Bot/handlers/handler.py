from aiogram import Router
from aiogram import F
from aiogram.fsm.state import StatesGroup

from TgBotStars.Bot.keyboard.keyboard import get_kb

from aiogram import Bot, types
from aiogram.filters import Command
from Sample.ENV import env

rt = Router()

# - - - Состояния - - -
class BotStates(StatesGroup):
    pass

# - - - Хендлеры - - -
@rt.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет", reply_markup=get_kb())

@rt.message(F.text)
async def request(message: types.Message):
    await message.answer(message.html_text)

