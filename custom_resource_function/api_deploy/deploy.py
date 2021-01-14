import json

import boto3
import cfnresponse


def handler(event, context):
    print(f"event: {json.dumps(event)}")
    client = boto3.client('apigateway')
    status = cfnresponse.SUCCESS
    stage_name = event.get("ResourceProperties", {}).get("StageName")
    api_gateway_id = event.get("ResourceProperties", {}).get("ApiGatewayId")
    print(f"Request Type: {event.get('RequestType')}")
    if event.get("RequestType") == "Delete":
        print(f"Delete Request: {event}")
        cfnresponse.send(
            event=event,
            context=context,
            responseStatus=cfnresponse.SUCCESS,
            responseData={}
        )
    elif event.get("RequestType") in ["Create", "Update"]:
        try:
            print(f"creating stage: {stage_name} for api gateway: {api_gateway_id}")
            response = client.create_deployment(
                restApiId=api_gateway_id,
                stageName=stage_name
            )
            deployment_id = response.get("id")
            response_data = {
                "stage": stage_name
            }
        except Exception as e:
            print(f"An error has occurred: ${str(e)}")
            response_data = {
                "error": str(e)
            }
            status = cfnresponse.FAILED
        finally:
            cfnresponse.send(
                event=event,
                context=context,
                responseStatus=status,
                responseData=response_data
            )
    else:
        # TODO think about this again
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
