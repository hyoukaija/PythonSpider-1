import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'http://www.wandoujia.com/apps/com.tencent.mm/comment'

user_agent = UserAgent()

# 获取页面源码
def get_page(url):
    headers = {
        'User-Agent': user_agent.random
    }
    request = Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
    except HTTPError as e:
        print(e.reason)
    except URLError as e:
        print(e.reason)
    else:
        return response.read().decode('utf-8')

# 提取每页数据
def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.select('.normal-li')
    for li in lis:
        result = {
            'name': li.select('.name')[0].get_text().strip(),
            'comment': li.select('.cmt-content')[0].get_text().strip()
        }
        yield result

if __name__ == "__main__":
    result = []
    for i in range(1, 10+1):
        url = base_url + str(i)
        for item in parse_page(get_page(url)):
            print(item)
            result.append(item)
    pd.DataFrame(result).to_csv('data1.csv')