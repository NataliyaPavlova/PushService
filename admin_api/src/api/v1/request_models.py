from datetime import datetime

from pydantic import BaseModel, Extra


class RequestBase(BaseModel):
    """Базовый класс для моделей запросов.
    Запрещена передача полей не предусмотренных схемой."""

    class Config:
        extra = Extra.forbid


class PushRequestCreate(RequestBase):
    headings: dict
    contents: dict
    push_type: str


class CampaignRequestCreate(RequestBase):
    users: list[str]
    push: PushRequestCreate
    started_at: datetime
    finished_at: datetime


