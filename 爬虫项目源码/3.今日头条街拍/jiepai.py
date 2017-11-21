import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from urllib.parse import urlencode
import json

base_url = 'https://www.toutiao.com/search_content/?'

user_agent = UserAgent()

# 构建请求url
def make_url(offset=0, keyword='街拍'):
    query = {
        'offset': str(offset),
        'format': 'json',
        'keyword': str(keyword),
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
    }
    url = base_url + urlencode(query)
    return url

# 获取json数据
def get_json(url):
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
        return json.loads(response.read().decode('utf-8'))

# 获取图片
def get_pic(url):
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
        return response.read()

# 提取图片地址
def parse_json(json):
    if 'data' in json:
        data = json.get('data')
        for item in data:
            image_detail = item.get('image_detail')
            if image_detail:
                for image in image_detail:
                    url_list = image.get('url_list')
                    if url_list:
                        for pic in url_list:
                            yield pic['url']


# 保存至文件
def save_to_file(item, filename):
    with open('Images/'+filename, 'wb') as f:
        f.write(item)

if __name__ == "__main__":
    for i in range(5):
        for pic_url in parse_json(get_json(make_url(offset=i))):
            save_to_file(get_pic(pic_url), '%s.jpg' % pic_url.split('/')[-1])
            print('正在下载：',pic_url)