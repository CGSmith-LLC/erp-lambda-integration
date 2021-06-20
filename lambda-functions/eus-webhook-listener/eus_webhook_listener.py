import json
import xml.etree.ElementTree as ET


def lambda_handler(event, context):
    # TODO implement
    # print("event --> ", event)

    try:
        body = event['body']
    except Exception as e:
        print("Failed to extract message body: ", e)
        return {
            'statusCode': 500,
            'message': json.dumps("Failed to extract message body. Please contact your administrator.")
        }
    else:
        parsed_xml = parse_xml(body)
        print(parsed_xml)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


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
    return et


if __name__ == "__main__":
    event = {
        "resource": "/tempListener",
        "path": "/tempListener",
        "httpMethod": "POST",
        "headers": {
            "Content-Type": "text/xml;charset=utf-16",
            "Host": "oe74yufi00.execute-api.us-east-2.amazonaws.com",
            "X-Amzn-Trace-Id": "Root=1-60cf85c9-2e5f19697c64035407e729e5",
            "X-Forwarded-For": "139.60.210.1",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "multiValueHeaders": {
            "Content-Type": [
                "text/xml;charset=utf-16"
            ],
            "Host": [
                "oe74yufi00.execute-api.us-east-2.amazonaws.com"
            ],
            "X-Amzn-Trace-Id": [
                "Root=1-60cf85c9-2e5f19697c64035407e729e5"
            ],
            "X-Forwarded-For": [
                "139.60.210.1"
            ],
            "X-Forwarded-Port": [
                "443"
            ],
            "X-Forwarded-Proto": [
                "https"
            ]
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "24yhxb",
            "resourcePath": "/tempListener",
            "httpMethod": "POST",
            "extendedRequestId": "BPHXgEeICYcFTqg=",
            "requestTime": "20/Jun/2021:18:15:37 +0000",
            "path": "/dev/tempListener",
            "accountId": "406186376066",
            "protocol": "HTTP/1.1",
            "stage": "dev",
            "domainPrefix": "oe74yufi00",
            "requestTimeEpoch": 1624212937447,
            "requestId": "03376ae9-d979-4c96-939e-5027b5941ccd",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "sourceIp": "139.60.210.1",
                "principalOrgId": None,
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": None,
                "user": None
            },
            "domainName": "oe74yufi00.execute-api.us-east-2.amazonaws.com",
            "apiId": "oe74yufi00"
        },
        "body": "<?xml version='1.0' encoding='utf-8'?>\r\n            <Towercoverage>\r\n            <CustomerDetails><apikey>test</apikey> <username>43</username> <password>2</password> <FirstName>Chris</FirstName>  <LastName>Smith</LastName> <StreetAddress>917 Main Street</StreetAddress> <CustomerLat>42.8531</CustomerLat> <CustomerLong>-88.3341</CustomerLong> <City>Mukwonago</City> <State>WI</State> <Country>US</Country> <ZIP>53149</ZIP> <PhoneNumber>262-220-7784</PhoneNumber> <EmailAddress>chris@cgsmith.net</EmailAddress> <HearAbout>Word of Mouth</HearAbout> <ContactMethod>Mail</ContactMethod> <ContactTime>Anytime</ContactTime> <Comment>Test for comments</Comment> <fiberincludes></fiberincludes> <CustomerLinkInfo> </CustomerLinkInfo></CustomerDetails></Towercoverage>",
        "isBase64Encoded": False
    }

    lambda_handler(event, "")

