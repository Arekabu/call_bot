from parser.exceptions import BaseServiceException, Server500
from typing import final

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import RegistrationStates
from services.base import BaseService


@final
class RegistrationStartService(BaseService):
    """Сервис начала регистрации"""

    async def _get_telegram_id(self, message: Message, state: FSMContext) -> str:
        return str(message.from_user.id)

    async def _call_api(
        self, telegram_id: str, message: Message, state: FSMContext
    ) -> None:
        await message.answer("Введите адрес электронной почты пользователя.")
        await state.set_state(RegistrationStates.waiting_for_email)


@final
class RegistrationEmailService(BaseService):
    """Сервис отправки email"""

    async def _get_telegram_id(self, message: Message, state: FSMContext) -> str:
        return str(message.from_user.id)

    async def _call_api(
        self, telegram_id: str, message: Message, state: FSMContext
    ) -> None:
        """Отправка введённого email на сервер"""
        email = message.text.strip()
        telegram_id = str(message.from_user.id)

        try:
            # Отправляем запрос на сервер
            await self.api.send_email(email, telegram_id)

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


@final
class RegistrationCodeService(BaseService):
    """Сервис отправки кода"""

    async def _get_telegram_id(self, message: Message, state: FSMContext) -> str:
        return str(message.from_user.id)

    async def _call_api(
        self, telegram_id: str, message: Message, state: FSMContext
    ) -> None:
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
            response_data = await self.api.send_code(code, telegram_id)

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
