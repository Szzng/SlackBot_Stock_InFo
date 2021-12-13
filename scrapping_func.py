import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import datetime

def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = bs(res.text, 'lxml')
    return soup

def get_edaily_news():
    standard_time = (datetime.datetime.today() - datetime.timedelta(hours=1.05)).strftime('%H:%M')
    context = []
    today = datetime.datetime.today().strftime('%Y%m%d')
    todaynews_url = f'https://www.edaily.co.kr/articles/stock/item/{today}'
    soup = create_soup(todaynews_url)
    news_list = soup.find('div', id='newsList').find_all('div', class_='newsbox_04')

    for idx, news in enumerate(news_list[::-1]):
        wdate = news.find('div', class_='author_category').get_text()
        re_d = re.sub('[\D]', '', wdate)
        wdate = re_d[2:4] + '월 ' + re_d[4:6] + '일 ' + re_d[6:8] + ':' + re_d[8:]
        if standard_time < wdate[-5:]:
            a = news.find('a')
            title = a['title']
            link = 'https://www.edaily.co.kr/' + a['href']
            context.append(f'\n{idx+1}. {title} \t({wdate})\n{link}\n')
    return context


def get_dart():
    kospi_url = 'https://dart.fss.or.kr/dsac001/mainY.do'
    kosdaq_url = 'https://dart.fss.or.kr/dsac001/mainK.do?selectDate=&sort=&series=&mdayCnt=0'
    own_url = 'https://dart.fss.or.kr/dsac001/mainO.do'

    standard_time = (datetime.datetime.today() - datetime.timedelta(hours=1.05)).strftime('%H:%M')
    context = []

    for idx, url in enumerate([kospi_url, kosdaq_url, own_url]):

        if idx == 0: context.append('# 코스피 #')
        elif idx == 1: context.append('# 코스닥 #')
        else: context.append('# 5%ㆍ임원보고 #')

        soup = create_soup(url)
        trs = soup.find('div', class_='tbListInner').find_all('tr')

        for tr in trs[::-1]:
            td = tr.find_all('td')
            if len(td) < 1: continue
            time = td[0].get_text().strip()
            if standard_time < time:
                pre = re.sub('\s', '', td[1].find('span').get_text().strip())
                category = pre[0]
                corp = pre[1:]
                a = td[2].find('a')
                report = re.sub('\s', '', a.get_text().strip())
                link = 'https://dart.fss.or.kr/' + a['href']

                context.append(f'* {time} \t({category}) {corp}\t{report}\n{link}')
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
