from parser.api_client import DjangoAPIClient
from parser.exceptions import BaseServiceException

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.states import RegistrationStates


class RegistrationService:
    def __init__(self):
        self.api_client = DjangoAPIClient()

    async def start_registration(self, message: Message, state: FSMContext) -> None:
        """Начало процесса регистрации"""
        await message.answer("Введите адрес электронной почты пользователя.")
        await state.set_state(RegistrationStates.waiting_for_email)

    async def process_email(self, message: Message, state: FSMContext) -> None:
        """Отправка введённого email на сервер"""
        email = message.text.strip()
        telegram_id = str(message.from_user.id)

        try:
            # Отправляем запрос на сервер
            await self.api_client.register_user(email, telegram_id)

            # Сохраняем email в состоянии
            await state.update_data(email=email)

            # Переходим к ожиданию кода
            await message.answer(f"Введите код, отправленный на email: {email}")
            await state.set_state(RegistrationStates.waiting_for_code)

        except BaseServiceException as e:
            # Отправляем полный текст ошибки от сервера
            await message.answer(e.send)
            await state.clear()

    async def process_code(self, message: Message, state: FSMContext) -> None:
        """Обработка введенного кода (заглушка)"""
        code = message.text.strip()
        user_data = await state.get_data()
        email = user_data.get("email", "неизвестный email")

        # Здесь будет логика проверки кода
        await message.answer(
            f"Код {code} для email {email} принят. " f"Дальше будет что-то ещё..."
        )
        await state.clear()
