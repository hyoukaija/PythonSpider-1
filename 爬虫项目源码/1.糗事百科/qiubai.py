import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from lxml import etree

base_url = 'https://www.qiushibaike.com/8hr/page/'

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
    tree = etree.HTML(html)
    result = tree.xpath('//div[@class="content"]/span/text()')
    return result

if __name__ == "__main__":
    start_page = int(input("请输入起始页："))
    end_page = int(input("请输入终止页："))
    for i in range(start_page, end_page + 1):
        print(parse_page(get_page(base_url + str(i))))