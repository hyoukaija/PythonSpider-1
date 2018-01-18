import requests
from fake_useragent import UserAgent
import re
import pymongo
import time
import random

user_agent = UserAgent()
base_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{page}.html'
domain = 'http://www.ygdy8.net'

client = pymongo.MongoClient(host='localhost')
db = client['Movies']
coll = db['Lastest']


def generate_headers():
    headers = {
        'User-Agent': user_agent.random
    }
    return headers


def get_html(url):
    headers = generate_headers()
    response = requests.get(url, headers=headers)
    response.encoding = 'gb2312'
    return response.text


def parse_download(html):
    return {
        'name':re.findall('<div class="title_all"><h1><font color=#07519a>(.*?)</font></h1></div>', html)[0],
        "url":re.findall('<a href="(.*?)">.*?</a></td>', html)[0]
    }


def parse_link(html):
    return re.findall('<a href="(.*?)" class="ulink">', html)


def save_to_mongodb(item):
    coll.insert_one(item)


if __name__ == '__main__':
    for i in range(1, 170):
        for link in parse_link(get_html(base_url.format(page=str(i)))):
            item = parse_download(get_html(domain + link))
            save_to_mongodb(item)
            print(item)
        time.sleep(random.choice([1, 2]))