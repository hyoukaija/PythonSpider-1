import requests
from fake_useragent import UserAgent
from lxml import etree
import pandas as pd

user_agent = UserAgent()
base_url = 'https://www.lagou.com/zhaopin/Python/{page}/?filterOption={id}'


def generate_headers():
    headers = {
        'User-Agent': user_agent.random
    }
    return headers


def get_html(url):
    headers = generate_headers()
    response = requests.get(url, headers=headers)
    return response.text


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


if __name__ == '__main__':
    jobs = []
    for i in range(1, 10):  # 调整页数
        for item in parse_html(get_html(base_url.format(page=str(i), id=str(i)))):
            print(item)
            jobs.append(item)

    jobs = pd.DataFrame(jobs)
    jobs.to_csv('jobs.csv', header=False, index=False)