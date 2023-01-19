import enum
from pydantic import BaseModel
from core.settings import get_settings

settings = get_settings()


class Log(BaseModel):
    class Event(str, enum.Enum):
        REMAINING = "remaining"
        SUCCESSFUL = "successful"
        FAILED = "failed"
        ERRORED = "errored"
        CONVERTED = "converted"
        RECEIVED = "received"

    notification_id: str
    campaign_id: int
    push_id: int
    push_tokens: list[str]
    created_at: str
    event: str
    number_of_events: int
    completed_at: str | None
