from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from Bot.keyboard.keyboard import get_kb
from ENV.env import BOT_TOKEN
import logging

logger = logging.getLogger(__name__)
rt = Router()


# ===== FSM States =====
class UserStates(StatesGroup):
    """States for user interaction flow"""
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_age = State()
    waiting_for_sports = State()
    waiting_for_allergies = State()
    waiting_for_budget = State()
    waiting_for_goal = State()
    waiting_for_preferences = State()
    waiting_for_duration = State()


# ===== Command Handlers =====
@rt.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Handle /start command"""
    welcome_text = (
        "🥗 Добро пожаловать в Nutrition Bot!\n\n"
        "Я помогу вам составить идеальный план питания на основе:\n"
        "✅ Ваших физических параметров\n"
        "✅ Целей\n"
        "✅ Предпочтений\n"
        "✅ Бюджета\n\n"
        "Нажмите кнопку ниже, чтобы начать!"
    )
    await message.answer(welcome_text, reply_markup=get_kb())


@rt.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handle /help command"""
    help_text = (
        "📖 Команды бота:\n\n"
        "/start - Начать создание плана питания\n"
        "/help - Показать справку\n"
        "/profile - Мой профиль\n"
        "/plans - Мои планы питания\n\n"
        "Или просто напишите свой вопрос о питании!"
    )
    await message.answer(help_text)


@rt.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Handle /profile command"""
    profile_text = "👤 Профиль пользователя\n\nЗаполните анкету, нажав 'Начать' в главном меню."
    await message.answer(profile_text)


@rt.message(F.text == "Привет")
async def greeting(message: types.Message):
    """Handle greeting"""
    await message.answer("👋 Привет! Рад вас видеть!", reply_markup=get_kb())


@rt.message(F.text == "Пока")
async def goodbye(message: types.Message):
    """Handle goodbye"""
    await message.answer("👋 До встречи! Будьте здоровы!")


@rt.message(F.text)
async def echo(message: types.Message):
    """Echo user message"""
    await message.answer(f"Вы написали: {message.text}")
