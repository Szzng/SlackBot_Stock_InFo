from slack_func import *
from scrapping_func import *

channel = '#이데일리뉴스'
token, headline = handle_slack_common_parts(channel)

for i in get_edaily_news():
    post_slack_message(token, channel, i)

print(channel, headline)