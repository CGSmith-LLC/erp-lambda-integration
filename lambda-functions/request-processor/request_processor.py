import json
import boto3

## Constants
SQS = "sqs"

def lambda_handler(event, context):

    temp_sqs = "https://sqs.us-east-2.amazonaws.com/406186376066/eus-testing-queue"

    response = save_event_to_sqs(temp_sqs, event)

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


if __name__ == "__main__":
    event = {
        "temp": "value"
    }
    context = ""
    print(lambda_handler(event, context))
    