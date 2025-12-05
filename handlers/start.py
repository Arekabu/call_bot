from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main import get_main_inline_keyboard
from services import RegistrationStartService

router = Router()
registration_start_service = RegistrationStartService()


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = """
📞 *Добро пожаловать!*

Это бот для управления вашими созвонами.
Выберите действие:
    """
    await message.answer(
        text, parse_mode="Markdown", reply_markup=get_main_inline_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработка команды help"""

    help_text = """
    📚 *Помощь по командам*

*Основные команды:*

/start - Главное меню
/help - Эта справка
/register - Начать регистрацию

*Кнопки в меню:*

📅 Мои созвоны - Показать ваши созвоны на сегодня
📝 Регистрация - Зарегистрироваться
❓ Помощь - Показать эту справку

Для связи: help@me.please
        """
    await message.answer(help_text, parse_mode="Markdown")


@router.callback_query(F.data == "help")
async def help_button(callback: CallbackQuery):
    """Обработка нажатия кнопки Помощь"""
    await callback.answer()
    await cmd_help(callback.message)


@router.callback_query(F.data == "register")
async def register_button(callback: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки регистрации"""
    await callback.answer()
    await registration_start_service.execute(callback.message, state)
