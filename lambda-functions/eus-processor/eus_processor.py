import requests
import os
import json

EUS_SUBMISSION_URL = os.environ['EUS_SUBMISSION_URL']

def lambda_handler(event, context):

    print("event --> ", event)
    print("context --> ", context)

    processed_event = process_event(event)
    
    data = {}
    try:
        data["multicoverageid"] = processed_event["multicoverageid"]
        data["Account"] = processed_event["Account"]
        data["Firstname"] = processed_event["Firstname"]
        data["lastname"] = processed_event["lastname"]
        data["Address"] = processed_event["Address"]
        data["city"] = processed_event["city"]
        data["Country"] = processed_event["Country"]
        data["State"] = processed_event["State"]
        data["zipcode"] = processed_event["zipcode"]
        data["phonenumber"] = processed_event["phonenumber"]
        data["emailaddress"] = processed_event["emailaddress"]
        data["howdidyouhear"] = processed_event["howdidyouhear"]
        data["preferredmethod"] = processed_event["preferredmethod"]
        data["besttimetocontact"] = processed_event["besttimetocontact"]
        data["comments"] = processed_event["comments"]
        data["clientip"] = processed_event["clientip"]
        data["Latitude"] = processed_event["Latitude"]
        data["Longitude"] = processed_event["Longitude"]
        data["key"] = processed_event["key"]
    except Exception as e:
        print("Error Reading Params: ", e)
        return {
        'status_code': 400,
        'body': json.dumps("Failing to Read Params. Incomplete Params supplied.")
        }

    print("Posting Data: ", data)

    ## Post data to towercoverage
    response = post_data(data)

    ## Convert response to String
    response_content = response.content.decode("utf-8")
    print(response_content)
    print(response.status_code)

    if ("Error Code" in response_content):
        error_message = response_content.split("Message:")[1].split("</string>")[0]
        return {
            'status_code': 400,
            'message': json.dumps(error_message)
        }

    ## Getting Content


    return {
        'status_code': 200,
        'body': json.dumps("Success!!")
    }

def post_data(data):
    try:
        response = requests.post(EUS_SUBMISSION_URL, data)
        return response
    except Exception as e:
        print(e)

def removing_special_characters(value):
    if "%20" in value:
        value = value.replace("%20", " ")
    if "%40" in value:
        value = value.replace("%40", "@")
    return value

def process_event(event):
    body = event['body']
    result = {}
    for key_value in body.split("&"):
        key = key_value.split("=")[0]
        key = removing_special_characters(key)
        value = key_value.split("=")[1]
        value = removing_special_characters(value)
        result[key] = value
    return result
