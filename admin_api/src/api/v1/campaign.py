from http import HTTPStatus

from fastapi import APIRouter

from admin_api.src.api.v1.request_models import CampaignRequestCreate
from admin_api.src.api.v1.response_models import CampaignResponse
from core.utils import get_campaign_service_callback
from core.db_mysql.db import get_mysql_session

router = APIRouter(prefix="/api/v1/campaigns", tags=["Campaign"])


@router.post(
    '/start',
    response_model=CampaignResponse,
    response_model_exclude_none=True,
    status_code=HTTPStatus.CREATED,
    summary='Send push-notifications. Save campaign info in DB',
    response_description='Data about created campaign'
)
async def save_campaign(
        campaign: CampaignRequestCreate
) -> CampaignResponse:
    """
    Send push-notifications. Save campaign info in DB

    :param campaign: users (push tokens), pushes, started_at, finished_at
    """
    session = get_mysql_session()
    campaign_service = await get_campaign_service_callback(session)
    created_campaign, created_push = await campaign_service.save_campaign(campaign)

    return CampaignResponse(
        started_at=created_campaign.started_at,
        finished_at=created_campaign.finished_at,
        push_headings=created_push.headings,
        users=created_campaign.users
    )

