import logging
from datetime import datetime
from typing import Any

from app.mongo import manage_mongo_docs
from fastapi import FastAPI

from app.utils.settings import settings
from app.utils.schema import StatusResponse

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MediaServer",
    description="MediaServer Project",
    version="1.0.0",
)

app.include_router(manage_mongo_docs.router, prefix="/api/v1")

@app.get("/", response_model=StatusResponse, summary="Health Check")
async def health_check() -> dict[str, Any]:
    """
    Returns the operational status and current timestamp of the API.
    """
    return {"status": "ok", "datetime": str(datetime.now())}