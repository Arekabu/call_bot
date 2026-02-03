from pydantic import BaseModel, ConfigDict, Field


@dataclass(kw_only=True, slots=True, frozen=True)
class BaseDTO:
    telegram_id: str


@dataclass(kw_only=True, slots=True, frozen=True)
class RegistrationEmailDTO(BaseDTO):
    email: str


@dataclass(kw_only=True, slots=True, frozen=True)
class RegistrationCodeDTO(BaseDTO):
    code: str


@dataclass(kw_only=True, slots=True, frozen=True)
class MeetingsDTO(BaseDTO):
    chat_id: str


@dataclass(kw_only=True, slots=True, frozen=True)
class UpdateTimeDTO(BaseDTO):
    chat_id: str
    time: str
