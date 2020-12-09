from fastapi import APIRouter

from common.logger import logger
from config import get_config

router = APIRouter()
app_config = get_config()


@router.get("/")
@router.get("/health-check")
def health_check():
    logger.info("Health-check endpoint was called")
    return {
        "api-status": "All Good!",
        "version": app_config.VERSION
    }
