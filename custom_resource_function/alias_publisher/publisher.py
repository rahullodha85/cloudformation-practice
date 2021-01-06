import json

import boto3
import cfnresponse


def handler(event, context):
    print(f"event: ${json.dumps(event)}")

    client = boto3.client('lambda')
    status = cfnresponse.SUCCESS
    lambda_arn = event.get("ResourceProperties", {}).get("LambdaArn")
    alias_name = event.get("ResourceProperties", {}).get("AliasName")
    try:
        print(f"publishing a version for lambda: {lambda_arn}")
        response = client.publish_version(
            FunctionName=lambda_arn
        )
        version = response.get("Version")
        response = client.create_alias(
            FunctionName=lambda_arn,
            FunctionVersion=version,
            Name=alias_name
        )
        alias_arn = response.get("AliasArn")
        response_data = {
            "alias": alias_arn
        }
    except Exception as e:
        print(f"An error has occurred: ${e}")
        response_data = {
            "error": e
        }
        status = cfnresponse.FAILED
    finally:
        cfnresponse.send(
            event=event,
            context=context,
            responseStatus=status,
            responseData=response_data
        )
