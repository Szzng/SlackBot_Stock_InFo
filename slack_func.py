import os
import requests
from datetime import datetime


def post_slack_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text})
    # print(response)


def handle_slack_common_parts(channel):
    token = os.environ.get('SLACK_TOKEN')
    headline = '#' + str(datetime.today().strftime('%m월 %d일 %H시 %M분')) + '#'
    post_slack_message(token, channel, headline)
    return token, headline