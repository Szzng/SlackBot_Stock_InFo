import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from datetime import datetime

def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = bs(res.text, 'lxml')
    return soup


def post_slack_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text})
    print(response)


def get_edaily_news():
    today = datetime.today().strftime('%Y%m%d')
    todaynews_url = f'https://www.edaily.co.kr/articles/stock/item/{today}'
    soup = create_soup(todaynews_url)
    news_list = soup.find('div', id='newsList').find_all('div', class_='newsbox_04')
    context = []
    for idx, news in enumerate(news_list):
        a = news.find('a')
        title = a['title']
        link = 'https://www.edaily.co.kr/' + a['href']
        wdate = news.find('div', class_='author_category').get_text()
        re_d = re.sub('[\D]', '', wdate)
        wdate = re_d[2:4] + '월 ' + re_d[4:6] + '일 ' + re_d[6:8] + ':' + re_d[8:]
        context.append(f'\n{idx + 1}. {title} \t({wdate})\n{link}\n')
    return context

def get_IPO_info():
    df = pd.DataFrame(columns=['코', '이름', '공모가', '업종', '주관사', '경쟁률', '청약일정', '상장일'])
    soup = create_soup('https://finance.naver.com/sise/ipo.nhn')
    table = soup.find('div', id='contentarea').find_all('div', class_='item_area')
    for t in table:
        name = t.find('h4', class_='item_name').get_text().strip()
        price = t.find('li', class_='area_price').find('span').get_text().strip()
        busi = re.sub('\s', '', t.find('li', class_='area_type').get_text().strip())[2:]
        sup = re.sub('\s', '', t.find('li', class_='area_sup').get_text().strip())[3:]
        if t.find('li', class_='area_competition'):
            competition = t.find('li', class_='area_competition').find('span').get_text().strip()
        else:
            competition = '-'
        private = re.sub('\s', '', t.find('li', class_='area_private').get_text().strip())[4:]
        if len(private) < 3: break
        date = re.sub('\s', '', t.find('li', class_='area_list').get_text().strip())[3:]
        df.loc[len(df)] = [name[2:3], name[3:], price, busi, sup, competition, private, date]

    return df.to_markdown()


def slack(token):
    headline = '## ' + str(datetime.today().strftime('%Y년 %m월 %d일')) + '\t이데일리 뉴스 목록 ##'
    post_slack_message(token, "#이데일리뉴스", headline)
    for i in get_edaily_news():
        post_slack_message(token, "#이데일리뉴스", i)

    post_slack_message(token, "#이데일리뉴스", '## 기업 IPO ##')
    post_slack_message(token, "#이데일리뉴스", get_IPO_info())
