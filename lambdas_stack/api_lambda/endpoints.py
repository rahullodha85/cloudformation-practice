from fastapi import APIRouter

from common.logger import logger

router = APIRouter()

@router.get("/")
@router.get("/health-check")
def health_check():
    logger.info("Health-check endpoint was called")
    return {"api-status": "All Good!"}
