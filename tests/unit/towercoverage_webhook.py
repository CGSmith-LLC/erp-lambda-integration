import json
import pytest

from eus_processor import main


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    f = open("../../events/towercoverage_webhook/sample_event_1.json")
    data = json.load(f)

    return data


def test_lambda_handler(apigw_event, mocker):

    ret = main.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"
    # assert "location" in data.dict_keys()
