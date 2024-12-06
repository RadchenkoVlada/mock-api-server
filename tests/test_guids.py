from tests.request_utilities import execute_put, execute_get, execute_post
from tests.constants import HTTP_STATUS_CODES
import json, pytest

TEST_GUID_ADD_URL = "12345678-abcd-ef01-2345-6789abcde-aka"


@pytest.fixture(autouse=True)
def clear_guids():
    """
    This fixture is run before each test case.
    It's required in order to clean the internal guids data in the mock server,
    so all tests can run independently and reliably
    """
    with open("tests/test_data/PUT_guids_empty_list.json", 'r') as data_file:
        empty_guids = json.load(data_file)
    put_response = execute_put("/guids", empty_guids)
    assert put_response.status_code == 200


def test_post_guid_add():
    """
    Verifying positive case: that response return valid body and status for POST request which contain guid in URL.
    """
    post_response = execute_post(f"/{TEST_GUID_ADD_URL}/add")
    print("post_response.json()=", post_response.json())
    assert post_response.status_code == 200
    assert TEST_GUID_ADD_URL in post_response.json()['guids']


def test_post_guid_add_without_guid():
    """
    Verifying negative case: that response return status 404 for POST request which contain no guid in URL.
    """
    post_response = execute_post(f"//add")
    assert post_response.status_code == 404


@pytest.mark.parametrize("status_code", HTTP_STATUS_CODES)
def test_put_get_guids(status_code: int):
    """
    Test guids functionality of mock-api-server.
    GET request should be called always after PUT, because PUT can change status code and response of GET.
    Thus GET can't be tested separately
    """
    with open("tests/test_data/PUT_guids_positive.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    expected_data_json["status_code"] = status_code


    put_response = execute_put(f"/guids", expected_data_json)
    put_response_json = put_response.json()
    assert put_response.status_code == 200
    assert put_response_json["new_status_code"] == status_code
    assert put_response_json["new_body"] == expected_data_json["body"]

    get_rsp = execute_get(f"/guids")

    assert get_rsp.status_code == expected_data_json["status_code"]
    assert get_rsp.json() == expected_data_json["body"]

def test_put_guids_without_key_body():
    """
    Negative test for PUT guids functionality of mock-api-server.
    PUT request shouldn't contain the key body,but contain the key status_code.
    """
    with open("tests/test_data/PUT_guids_without_key_body.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    put_response = execute_put("/guids", expected_data_json)
    assert put_response.status_code == 500


def test_put_guids_without_key_status_code():
    """
    Negative test for PUT guids functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    """
    with open("tests/test_data/PUT_guids_without_key_status_code.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)

    put_response = execute_put("/guids", expected_data_json)
    assert put_response.status_code == 500


def test_put_guids_without_request_body():
    """
    Negative test for PUT guids functionality of mock-api-server.
    PUT request body should contain both body and status_code.
    In this case PUT request doesn't have any content.
    """
    put_response = execute_put("/guids")
    assert put_response.status_code == 400


def test_post_several_items():
    """
    Test POST request by adding several guids(one at a time) to guids list.
    Then verifying guids list using GET request
    """
    for _ in range(5):
        post_response = execute_post(f"/{TEST_GUID_ADD_URL}/add")
        print("post_response.json()=", post_response.json())
        assert post_response.status_code == 200
        assert TEST_GUID_ADD_URL in post_response.json()['guids']

    get_rsp = execute_get(f"/guids")
    assert get_rsp.status_code == 200
    assert get_rsp.json()['guids'] == [TEST_GUID_ADD_URL] * 5


def test_get_guids():
    with open("tests/test_data/PUT_guids_empty_list.json", 'r') as expected_data_file:
        expected_data_json = json.load(expected_data_file)
    get_rsp = execute_get(f"/guids")
    assert get_rsp.status_code == expected_data_json["status_code"]
    assert get_rsp.json() == expected_data_json["body"]
