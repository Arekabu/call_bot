from pydantic import BaseModel, ConfigDict, Field


class BaseDTO(BaseModel):
    telegram_id: str = Field(exclude=True)

    model_config = ConfigDict(frozen=True, extra="forbid")


class RegistrationEmailDTO(BaseDTO):
    email: str


class RegistrationCodeDTO(BaseDTO):
    code: str


class MeetingsDTO(BaseDTO):
    chat_id: str


class UpdateTimeDTO(BaseDTO):
    chat_id: str
    time: str
