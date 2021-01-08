import json
from datetime import datetime

import boto3
from fastapi import APIRouter

from common.logger import logger
from config import get_config
from common.models import MessageIn

router = APIRouter()
app_config = get_config()


@router.get("/")
@router.get("/health-check")
def health_check():
    logger.info("Health-check endpoint was called")
    return {
        "api-status": "All Good! test",
        "version": app_config.VERSION
    }


@router.post("/send")
def send_message(message_in: MessageIn):
    queue_payload = {
        "message": message_in.message
    }
    sqs_client = boto3.client(
        "sqs",
        endpoint_url=app_config.SQS_ENDPOINT_URL
    )
    datetime_stamp = datetime.now().timestamp() * 1000
    logger.info(f"sending message to queue: {app_config.QUEUE_URL}")
    queue_response = sqs_client.send_message(
        QueueUrl=app_config.QUEUE_URL,
        MessageBody=json.dumps(queue_payload),
        MessageGroupId="cf-test",
        MessageDeduplicationId=f"cf-test-{datetime_stamp}"
    )
    logger.info(f"queue response: {json.dumps(queue_response)}")

    return {
        "response": {
            "message_id": queue_response.get("MessageId")
        }
    }
