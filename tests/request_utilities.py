import json
import requests
from tests.constants import BASE_URL_HTTP, BASE_URL_HTTPS, HEADERS


global_config = None

def get_config():
    global global_config
    if global_config is None:
        with open("tests/test_config.json", 'r') as f:
            global_config = json.load(f)
    return global_config


def execute_get(url):
    config = get_config()
    if config["use_https"]:
        return requests.get(BASE_URL_HTTPS + url, verify=config["https_config"]["cert_file"])
    else:
        return requests.get(BASE_URL_HTTP + url)


def execute_post(url):
    config = get_config()
    if config["use_https"]:
        return requests.post(BASE_URL_HTTPS + url, headers=HEADERS, verify=config["https_config"]["cert_file"])
    else:
        return requests.post(BASE_URL_HTTP + url, headers=HEADERS)


def execute_put(url, body=None):
    config = get_config()
    if config["use_https"]:
        return requests.put(BASE_URL_HTTPS + url, headers=HEADERS, json=body, verify=config["https_config"]["cert_file"])
    else:
        return requests.put(BASE_URL_HTTP + url, headers=HEADERS, json=body)

