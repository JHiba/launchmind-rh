import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_slack_message(text):
    webhook = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook:
        print(" No Slack webhook found in .env")
        return

    response = requests.post(webhook, json={"text": text})

    if response.status_code == 200:
        print("Slack message sent")
    else:
        print(" Slack error:", response.status_code, response.text)