import requests
import json

BASE_URL = "http://api-mock-server:80"

def test_get_inventory_appliances():
    """
    Test inventory GET request for mock-api-server
    """
    with open("tests/test_data/GET_devices.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    rsp = requests.get(f"{BASE_URL}/inventory/devices")

    assert rsp.status_code == 200
    assert expected_data_json == rsp.json()
