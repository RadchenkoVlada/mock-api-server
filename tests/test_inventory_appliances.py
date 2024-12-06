from tests.request_utilities import execute_put, execute_get
from tests.constants import HTTP_STATUS_CODES
import json, pytest


@pytest.mark.parametrize("status_code", HTTP_STATUS_CODES)
def test_put_get_inventory_appliances(status_code: int):
    """
    Test inventory functionality of mock-api-server.
    GET request should be called always after PUT, because PUT can change status code and response of GET.
    Thus GET can't be tested separately
    """
    with open("tests/test_data/PUT_inventory_positive.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    expected_data_json["status_code"] = status_code

    put_response = execute_put("/inventory/devices", expected_data_json)
    put_response_json = put_response.json()
    assert put_response.status_code == 200
    assert put_response_json["new_status_code"] == status_code
    assert put_response_json["new_body"] == expected_data_json["body"]

    get_rsp = execute_get("/inventory/devices")

    assert get_rsp.status_code == expected_data_json["status_code"]
    assert get_rsp.json() == expected_data_json["body"]

def test_put_inventory_without_key_body():
    """
    Negative test for PUT inventory functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    """
    with open("tests/test_data/PUT_inventory_without_body.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    put_response = execute_put("/inventory/devices", expected_data_json)
    assert put_response.status_code == 500

def test_put_inventory_without_key_status_code():
    """
    Negative test for PUT inventory functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    """
    with open("tests/test_data/PUT_inventory_without_status_code.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    put_response = execute_put("/inventory/devices", expected_data_json)
    assert put_response.status_code == 500


def test_put_inventory_without_request_body():
    """
    Negative test for PUT inventory functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    In this case PUT request doesn't have any content.
    """
    put_response = execute_put("/inventory/devices")
    assert put_response.status_code == 400
