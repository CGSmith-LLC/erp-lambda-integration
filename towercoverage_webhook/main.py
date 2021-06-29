import json
import xml.etree.ElementTree as ET
import boto3
import os

SQS = 'sqs'
SSM = 'ssm'
PARAMETER_NAME = os.environ['SQS_QUEUE_PATHS']

def lambda_handler(event, context):
    # TODO implement
    print("event --> ", event)

    ssm_client = get_service_client(SSM)
    if ssm_client:
        parameter_value = json.loads(get_parameter(ssm_client, PARAMETER_NAME))
        sqs_queues = parameter_value['SQS_QUEUES']
    try:
        WEBHOOK_EVENT_QUEUE_URL = sqs_queues['WEBHOOK_EVENT_QUEUE_URL']
        WEBHOOK_EVENT_QUEUE_NAME = sqs_queues['WEBHOOK_EVENT_QUEUE_NAME']
    except Exception as e:
        print("Error reading parameter Store: ", e)
        return {
            'statusCode': 500,
            'message': json.dumps('Failed to get parameters.')
        }
        exit(1)

    try:
        body = event['body']
    except Exception as e:
        print("Failed to extract message body: ", e)
        return {
            'statusCode': 500,
            'message': json.dumps("Failed to extract message body. Please contact your administrator.")
        }
    else:
        text_map = parse_xml(body)
        print(text_map)

    try:
        response = save_event_to_sqs(WEBHOOK_EVENT_QUEUE_URL, text_map)
        print("Event Added: ", response)
    except Exception as e:
        print("Failed to put event to queue: ", e)
        return {
            'statusCode': 500,
            'message': json.dumps("Failed to put event to SQS queue")
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Event added to SQS queue.')
    }

def get_service_client(service_name):
    return boto3.client(service_name)

def save_event_to_sqs(queue_url, message_body):
    sqs_client = get_service_client(SQS)
    message_str = json.dumps(message_body)
    message_request = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_str)
    return message_request

def get_parameter(client, parameter_name):
    """Fetch and return parameters from the parameter store"""
    try:
        params = client.get_parameter(Name=parameter_name)
    except Exception as e:
        print("Recevied Error: %s", e)
        return False
    else:
        try:
            response = json.loads(params["Parameter"]["Value"])
            print(response)
            return response
        except Exception as e:
            print("Received Error: %s", e)
            print("JSON is malformed, Kindly provide a valid JSON")
            return False


def parse_xml(xml_data):
    et = ET.fromstring(xml_data)
    print([elem.tag for elem in et.iter() if elem is not et])
    parent_map = {c: p.tag for p in et.iter() for c in p}
    text_map = {}
    for key in parent_map:
        if parent_map[key] == "CustomerDetails":
            text_map[key.tag] = key.text
        

    print("Parent Map:", parent_map)
    print("Text Map: ", text_map)
    return text_map
