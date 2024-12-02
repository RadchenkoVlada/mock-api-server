import requests
import json
import pytest


BASE_URL = "http://api-mock-server:80"
HEADERS = {'Content-type': 'application/json'}
HTTP_STATUS_CODES = list(range(200, 204)) + list(range(205, 209)) + [226] + list(range(300, 304)) + \
                    list(range(305, 309)) + list(range(400, 419)) + list(range(421,427)) + [428, 429, 431, 451] + \
                    list(range(500, 509)) + [510, 511]


@pytest.mark.parametrize("status_code", HTTP_STATUS_CODES)
def test_put_get_inventory_appliances(status_code):
    """
    Test inventory functionality of mock-api-server.
    GET request should be called always after PUT, because PUT can change status code and response of GET.
    Thus GET can't be tested separately
    """
    with open("tests/test_data/PUT_positive.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    expected_data_json["status_code"] = status_code

    put_response = requests.put(f"{BASE_URL}/inventory/devices", headers=HEADERS, json=expected_data_json)
    put_response_json = put_response.json()
    assert put_response.status_code == 200
    assert put_response_json["new_status_code"] == status_code
    assert put_response_json["new_body"] == expected_data_json["body"]

    get_rsp = requests.get(f"{BASE_URL}/inventory/devices")

    assert get_rsp.status_code == expected_data_json["status_code"]
    assert get_rsp.json() == expected_data_json["body"]

def test_put_inventory_without_body():
    """
    Negative test for PUT inventory functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    """
    with open("tests/test_data/PUT_without_body.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    put_response = requests.put(f"{BASE_URL}/inventory/devices", headers=HEADERS, json=expected_data_json)
    assert put_response.status_code == 500

def test_put_inventory_without_status_code():
    """
    Negative test for PUT inventory functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    """
    with open("tests/test_data/PUT_without_status_code.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    put_response = requests.put(f"{BASE_URL}/inventory/devices", headers=HEADERS, json=expected_data_json)
    assert put_response.status_code == 500


def test_put_inventory_without_request_body():
    """
    Negative test for PUT inventory functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    In this case PUT request doesn't have any content.
    """
    put_response = requests.put(f"{BASE_URL}/inventory/devices", headers=HEADERS)
    assert put_response.status_code == 400
