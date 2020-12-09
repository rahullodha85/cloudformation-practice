import json
import logging
import os

import boto3


def init_logger():
    root_logger = logging.getLogger(__name__)
    logging.getLogger().setLevel("INFO")
    return root_logger


logger = init_logger()


def lambda_handler(event, context):
    record = event.get("Records")[0]
    receipt_handle = record.get("receiptHandle")
    sqs_client = boto3.client("sqs", endpoint_url=os.getenv("SQS_ENDPOINT_URL"))
    try:

        body = json.loads(record.get("body"))
        logger.info(f"Queue Message: {body}")
    except Exception as e:
        logger.error(f"An error has occurred: {e}")
    finally:
        sqs_client.delete_message(
            QueueUrl=os.getenv("QUEUE_URL"),
            ReceiptHandle=receipt_handle
        )