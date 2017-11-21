import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from lxml import etree

base_url = 'https://movie.douban.com/top250?start={page}&filter='

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
    result = tree.xpath('//div[@class="hd"]/a/span[1]/text()')
    return result

# 保存至文件
def save_to_file(item, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(item)

if __name__ == "__main__":
    for i in range(10):
        for item in parse_page(get_page(base_url.format(page=str(i*25)))):
            print(item)
            save_to_file(item+'\n', '豆瓣电影Top250.txt')