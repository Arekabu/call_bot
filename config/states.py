from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_code = State()


class MeetingsUpdateTimeStates(StatesGroup):
    waiting_for_time = State()
