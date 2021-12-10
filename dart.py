from slack_func import *
from scrapping_func import *

channel = '#최근공시'
token, headline = handle_slack_common_parts(channel)

for i in get_dart():
    post_slack_message(token, channel, i)

print(channel, headline)