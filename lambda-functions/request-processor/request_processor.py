import json
import boto3
from botocore.exceptions import ClientError

## Constants
SQS = "sqs"
PARAMETER_NAME = "sqs-queues-paths"
SSM = "ssm"

def lambda_handler(event, context):

    ssm_client = get_service_client(SSM)
    if ssm_client:
        parameter_value = json.loads(get_parameter(ssm_client, PARAMETER_NAME))
        sqs_queues = parameter_value['SQS_QUEUES']
    try:
        EUS_QUEUE_URL = sqs_queues['EUS_QUEUE_URL']
        EUS_QUEUE_NAME = sqs_queues['EUS_QUEUE_NAME']
        ERP_QUEUE_URL = sqs_queues['ERP_QUEUE_URL']
        ERP_QUEUE_NAME = sqs_queues['ERP_QUEUE_URL']
    except Exception as e:
        print("Error reading parameter store: ", e.message)
        exit(1)

    print(parameter_value)

    if event['type'] == EUS_QUEUE_NAME:
        response = save_event_to_sqs(EUS_QUEUE_URL, event)
        print(response)
    elif event['type'] == ERP_QUEUE_NAME:
        response = save_event_to_sqs(ERP_QUEUE_URL, event)
        print(response)

    return {
        'status': 200,
        'body': json.dumps("Testing Lambda Function")
    }

def get_service_client(service_name):
    return boto3.client(service_name)


def save_event_to_sqs(queue_url, message_body):
    sqs_client = get_service_client(SQS)
    message_str = json.dumps(message_body)
    message_request = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_str)
    return message_request

def get_parameter(client, parameter_name):
    """Fetch and return parameters from the parameters store"""
    try:
        params = client.get_parameter(Name=parameter_name)
    except ClientError as e:
        print("Received Error: %s", e)
        return False
    else:
        try:
            return json.loads(params['Parameter']['Value'])
        except Exception as e:
            print("Received Error: %s", e)
            print("Json is malformed, Kindly provide a valid JSON")
            return False



if __name__ == "__main__":
    event = {
        "type": "erp-queue"
    }

    event2 = {
        "type": "eus-queue"
    }
    context = ""
    print(lambda_handler(event, context))
    print(lambda_handler(event2, context))
    