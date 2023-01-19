from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from admin_api.src.api.v1 import campaign

app = FastAPI(
    title='Push Notification Service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(campaign.router)


@app.get("/healthcheck")
async def health_check():
    return ORJSONResponse(content={"message": "api ok"})


# def start_admin():
#     uvicorn.run(
#         'admin_api.src.main:app', host='0.0.0.0', port=8000,
#     )
