import json

import boto3
import cfnresponse


def delete_mapping(domain_name):
    client = boto3.client('apigateway')
    print(f"Deleting {domain_name} mappings")
    client.delete_base_path_mapping(
        domainName=domain_name,
        basePath="(none)"
    )


def delete_stage(stage_name, api_gateway_id):
    client = boto3.client('apigateway')
    print(f"Deleting stage: {stage_name}")
    try:
        client.delete_stage(
            restApiId=api_gateway_id,
            stageName=stage_name
        )
    except Exception as e:
        print(f"an error has occurred: {e}")


def handler(event, context):
    print(f"event: {json.dumps(event)}")
    client = boto3.client('apigateway')
    status = cfnresponse.SUCCESS
    api_gateway_id = event.get("ResourceProperties", {}).get("ApiGatewayId")
    preview_domain_name = event.get("ResourceProperties", {}).get("PreviewDomainName")
    prod_domain_name = event.get("ResourceProperties", {}).get("ProdDomainName")
    stage_to_delete = event.get("ResourceProperties", {}).get("StageToDelete")
    print(f"Request Type: {event.get('RequestType')}")
    print(f"stage to delete: {stage_to_delete}")
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
            print(f"Getting production mappings")
            response = client.get_base_path_mappings(
                domainName=prod_domain_name
            )
            prod_stage_name = next(item.get("stage") for item in response.get("items")) if response.get("items") else None
            print(f"Getting preview mappings")
            response = client.get_base_path_mappings(
                domainName=preview_domain_name
            )
            preview_stage_name = next(item.get("stage") for item in response.get("items"))
            if not prod_stage_name:
                prod_stage_name = preview_stage_name
                print(f"Mapping production to stage: {prod_stage_name}")
                prod_response = client.create_base_path_mapping(
                    domainName=prod_domain_name,
                    restApiId=api_gateway_id,
                    stage=prod_stage_name,
                    basePath="(none)"   # for a blank basepath "(none)" value is required, refer to boto3 documentation
                )
                preview_response = prod_response
            else:
                delete_mapping(preview_domain_name)
                delete_mapping(prod_domain_name)
                print(f"Mapping preview to stage: {prod_stage_name}")
                preview_response = client.create_base_path_mapping(
                    domainName=preview_domain_name,
                    restApiId=api_gateway_id,
                    stage=prod_stage_name,
                    basePath="(none)"  # for a blank basepath "(none)" value is required, refer to boto3 documentation
                )
                print(f"Mapping production to stage: {preview_stage_name}")
                prod_response = client.create_base_path_mapping(
                    domainName=prod_domain_name,
                    restApiId=api_gateway_id,
                    stage=preview_stage_name,
                    basePath="(none)"  # for a blank basepath "(none)" value is required, refer to boto3 documentation
                )
                delete_stage(
                    stage_name=stage_to_delete,
                    api_gateway_id=api_gateway_id
                )
            response_data = {
                "preview_stage": preview_response.get("stage"),
                "prod_stage": prod_response.get("stage")
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
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
