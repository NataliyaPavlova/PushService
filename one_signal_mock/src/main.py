from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from one_signal_mock.src.api.v1 import notifications


app = FastAPI(
    title='One Signal Service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(notifications.router)


@app.get("/healthcheck")
async def health_check():
    return ORJSONResponse(content={"message": "api ok"})


def start_one_signal_mock():
    uvicorn.run(
        'one_signal_mock.src.main:app', host='0.0.0.0', port=8088, reload=True,
    )
