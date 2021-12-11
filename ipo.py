from slack_func import *
from scrapping_func import *

channel = '#ipo일정'
token, headline = handle_slack_common_parts(channel)
post_slack_message(token, channel, get_IPO_info())

print(channel, headline)