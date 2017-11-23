import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from lxml import etree
from urllib.parse import urlencode
import json

base_url = 'https://chengdu.anjuke.com/sale/p{page}/?'
query = {
    'utm_term':'成都最新房价'
}
base_url = base_url + urlencode(query)

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
    items = tree.xpath('//li[@class="list-item"]')
    for item in items:
        yield {
            'title':item.xpath('./div[2]/div[1]/a/@title')[0],
            'size':item.xpath('./div[2]/div[2]/span[2]/text()')[0][:-2],
            'price':item.xpath('./div[3]/span[1]/strong/text()')[0]
        }

# 保存至文件
def save_to_file(item, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(item)


if __name__ == "__main__":
    for i in range(1, 10):
        url = base_url.format(page=str(i))
        html = get_page(url)
        for item in parse_page(html):
            save_to_file(json.dumps(item, ensure_ascii=False)+'\n', 'data.json')
            print(item)