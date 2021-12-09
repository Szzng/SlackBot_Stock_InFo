import os
from myfunc import *

token = os.environ.get('SLACK_TOKEN')

# 이데일리뉴스
headline = '##\t ' + str(datetime.today().strftime('%Y년 %m월 %d일 %H시 %M분')) +' \t##'
post_slack_message(token, "#이데일리뉴스", headline)
for i in get_edaily_news():
    post_slack_message(token, "#이데일리뉴스", i)

# IPO 일정
post_slack_message(token, "#ipo일정", headline)
post_slack_message(token, "#ipo일정", get_IPO_info())

print(headline, 'success')
# 최근 공시
