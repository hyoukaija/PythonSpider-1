import urllib.request
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from fake_useragent import UserAgent
from lxml import etree
import re
import time

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

# 提取电影主页链接
def parse_link(html):
    tree = etree.HTML(html)
    links = tree.xpath('//div[@class="hd"]/a/@href')
    return links

def save_to_file(item, filename='douban.csv'):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(item)

def parse_movie(html):
    tree = etree.HTML(html)
    return [tree.xpath('//*[@id="content"]/div[1]/span[1]/text()')[0],tree.xpath('//div[@id="content"]/h1/span[@property="v:itemreviewed"]/text()')[0],
            '/'.join(tree.xpath('//a[@rel="v:directedBy"]/text()')),'/'.join(tree.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')),
            '/'.join(tree.xpath('//a[@rel="v:starring"]/text()')),'/'.join(tree.xpath('//span[@property="v:genre"]/text()')),
            tree.xpath('//span[@property="v:initialReleaseDate"]/text()')[0],tree.xpath('//span[@property="v:runtime"]/text()')[0],
            tree.xpath('//strong[@property="v:average"]/text()')[0],tree.xpath('//span[@property="v:votes"]/text()')[0],
            re.search('<span class="pl">制片国家/地区:</span>(.*?)<br/>', html, re.S).group(1),
            re.search('<span class="pl">语言:</span>(.*?)<br/>', html, re.S).group(1),
            re.search('<span class="pl">又名:</span>(.*?)<br/>', html, re.S).group(1)]

if __name__ == "__main__":
    with open('douban.csv', 'a', encoding='utf-8') as f:
        f.write('排名,片名,导演,编剧,主演,类型,上映日期,片长,豆瓣评分,评价人数,制片地区/国家,语言,又名\n')
    for i in range(10):
        page = get_page(base_url.format(page=str(i*25)))
        links = parse_link(page)
        for link in links:
            try:
                html = get_page(link)
                item = parse_movie(html)
            except:
                continue
            print(item)
            save_to_file(','.join(item)+'\n')
            time.sleep(1)