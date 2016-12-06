from time import sleep

import requests
import base64
import json

# from apscheduler.schedulers.blocking import BlockingScheduler

# from config import APP, KEY, PROCESS
import sys

APP = "ss-data-staging"
PROCESS = "celery"
KEY = "bc50be81-14ef-42cf-ae05-841d8f505d6c"

# Generate Base64 encoded API Key
# BASEKEY = base64.b64encode(":" + KEY)
# Create headers for API call
HEADERS = {

    "Accept": "application/vnd.heroku+json; version=3",
    "Authorization": "Bearer " + KEY
}


def scale(quantity, size):
    payload = {
        "updates": [
            {
                "quantity": quantity,
                "size": size,
                "type": "web",
            },
            {
                "quantity": quantity,
                "size": size,
                "type": "celery",
            }
        ],
    }
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation"
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
        # result = requests.get(url, headers=HEADERS)
    except:
        print("test!")
        return None
    if result.status_code == 200:
        return "Success!"
    else:
        return "Failure"

def scale_down(type):
    payload = {
        "updates": [
            {
                "quantity": 1,
                "size": "hobby",
                "type": type,
            }
        ],
    }
    json_payload = json.dumps(payload)
    url = "https://api.heroku.com/apps/" + APP + "/formation"
    try:
        result = requests.patch(url, headers=HEADERS, data=json_payload)
        # result = requests.get(url, headers=HEADERS)
    except:
        print("test!")
        return None
    if result.status_code == 200:
        return "Success!"
    else:
        return "Failure"


def get_current_dyno_quantity():
    url = "https://api.heroku.com/apps/" + APP + "/formation"
    try:
        result = requests.get(url, headers=HEADERS)
        for formation in json.loads(result.text):
            current_quantity = formation["quantity"]
            return current_quantity
    except:
        return None


if __name__ == "__main__":
    scale(sys.argv[1], "standard-1X")
    print("check heroku for scale up")
    sleep(10)
    scale(0, "hobby")
    scale_down("web")
    scale_down("celery")
    sleep(30)
    print("check heroku for scale down")
    # scale_down(sys.argv[1])
