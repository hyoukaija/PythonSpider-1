import requests
from fake_useragent import UserAgent
from lxml import etree
import time
import csv

user_agent = UserAgent()
# base_url = 'https://www.lagou.com/zhaopin/Python/{page}'
base_url = "https://www.lagou.com"

def generate_headers():
    headers = {
        'User-Agent': user_agent.random
    }
    return headers


def get_html(url):
    headers = generate_headers()
    response = requests.get(url, headers=headers)
    return response.text

# 获取主页各种职位链接
def getLinks(html):
    html = etree.HTML(html)
    links = html.xpath('//div[@class="menu_sub dn"]//a/@href')
    return links



def parse_html(html):
    html = etree.HTML(html)
    items = html.xpath('//li[@class="con_list_item default_list"]')
    for item in items:
        yield (item.xpath('.//div[@class="company_name"]/a/text()')[0].strip(),
               item.xpath('.//span[@class="money"]/text()')[0].strip(),
               item.xpath('.//div[@class="p_bot"]/div[@class="li_b_l"]/text()')[-1].strip(),
               item.xpath('.//div[@class="li_b_r"]/text()')[0],
               item.xpath('.//div[@class="p_top"]/a/h3/text()')[0],
               item.xpath('//div[@class="p_top"]/a/span/em/text()')[0])


def saveToFile(item, filename="lagoujob.csv"):
    with open(filename, 'a', encoding='utf-8') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(item)

if __name__ == '__main__':
    links = getLinks(get_html(base_url))
    for link in links:
        for i in range(1, 30):  # 调整页数
            for item in parse_html(get_html(link+str(i))):
                print(item)
                saveToFile(item)
            time.sleep(2)