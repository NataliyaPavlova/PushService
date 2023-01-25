from datetime import datetime

from pydantic import BaseModel


class PushResponse(BaseModel):
    headings: dict
    contents: dict
    push_type: str


class CampaignResponse(BaseModel):
    users: list[str]
    push_headings: dict
    started_at: datetime
    finished_at: datetime
    app_name: str


class BaseResponseModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class StatsDeliveryStatusResponse(BaseModel):
    delivery_status: dict
    campaign_id: int


class StatsUserDistributionResponse(BaseModel):
    user_distribution: list[dict]
    campaign_id: int
