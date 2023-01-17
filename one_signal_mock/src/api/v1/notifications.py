import json
import random
import uuid
from datetime import datetime

from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])

batches = {}


@router.post(
    '/',
)
async def get_batch(
        request: Request,
):
    body = await request.body()
    data = json.loads(body)
    notification_id = str(uuid.uuid4())

    batches[notification_id] = data

    return {
        "id": notification_id,
        "recipients": 1,
        "external_id": None
    }


@router.get(
    '/{notification_id}',
)
async def get_batch(
        request: Request,
        notification_id: str,
        app_id: str,
):
    # if notification_id not in batches.keys():
    #     total_users = 100
    #     data = {"include_player_ids": ['pushtoken1', "pushtoken2"]}
    # else:
    data = [] # batches[notification_id]
    total_users = random.randrange(100, 150) #len(data['include_player_ids'])

    received = random.randrange(0, total_users)
    return {
        "remaining": 0,
        "successful": received,
        "failed": total_users - received,
        "errored": 0,
        "converted": 0.05 * received,
        "received": received,
        "platform_delivery_stats": 1,
        "completed_at": datetime.now(),
        "include_player_ids": []
    }
