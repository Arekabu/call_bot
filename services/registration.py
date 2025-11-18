from parser.api_client import DjangoAPIClient
from parser.exceptions import BaseServiceException, Server500

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
            await self.api_client.send_email(email, telegram_id)

            # Сохраняем email и telegram_id в состоянии
            await state.update_data(email=email)
            await state.update_data(telegram_id=telegram_id)

            # Переходим к ожиданию кода
            await message.answer(f"Введите код, отправленный на email: {email}")
            await state.set_state(RegistrationStates.waiting_for_code)

        except BaseServiceException as e:
            # Отправляем полный текст ошибки от сервера
            await message.answer(e.send)
            await state.clear()

    async def process_code(self, message: Message, state: FSMContext) -> None:
        """Отправка введенного кода на сервер"""
        code = message.text.strip()

        user_data = await state.get_data()
        email = user_data.get("email", "")
        telegram_id = user_data.get("telegram_id", "")

        # Проверка данных в state
        if not email or not telegram_id:
            await message.answer("Данные сессии утеряны. Начните регистрацию заново.")
            await state.clear()
            return

        # Отправляем запрос на сервер
        try:
            response_data = await self.api_client.send_code(code, telegram_id)

            await message.answer(
                response_data.get(
                    "confirm", f"✅ Регистрация для {email} завершена успешно!"
                )
            )
            await state.clear()

        except Server500 as e:
            await message.answer(e.send)
            await state.clear()

        # Для других ошибок оставляем state для возможности повторного ввода кода
        except BaseServiceException as e:
            await message.answer(e.send)
