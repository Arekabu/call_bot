from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TimeUpdateDTO:
    time: str
    chat_id: str
    telegram_id: str
