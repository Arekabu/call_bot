from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(slots=True, kw_only=True, frozen=True)
class Meeting:
    id: int
    title: str
    start_time: datetime
    end_time: datetime
    participants: List[str]
    description: Optional[str] = None
    location: Optional[str] = None


@dataclass(slots=True, kw_only=True, frozen=True)
class SyncResult:
    new_meetings: List[Meeting]
    updated_meetings: List[Meeting]
    deleted_meetings: List[Meeting]
