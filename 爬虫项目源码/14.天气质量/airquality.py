import requests
from scrapy.selector import Selector
from fake_useragent import UserAgent
from selenium import webdriver
from urllib.parse import urljoin
import time
import pymongo

MONGO_URI = 'localhost'
MONGO_DB = 'airquality'
# COLLECTION = 'airdata'
COLLECTION = 'airdaydata'

base_url = 'https://www.aqistudy.cn/historydata/'
ua = UserAgent()
browser = webdriver.Chrome()
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
coll = db[COLLECTION]


def random_header():
    return {
        'User-Agent':ua.random
    }


def get_city_list(url=base_url):
    response = requests.get(url, headers=random_header())
    selector = Selector(text=response.text)
    citysList = [urljoin(url, item) for item in
                 selector.xpath('//div[@class="panel panel-info"]//li/a/@href').extract()]
    return citysList


def get_city_page_source(url):
    browser.get(url)
    time.sleep(5)
    return browser.page_source


def parse_month_data(page_source, city_name):
    selector = Selector(text=page_source)
    trs = selector.xpath('//div[@class="container"]//tbody/tr')[1:]
    for tr in trs:
        item = {}
        item['city'] = city_name
        item['date'] = tr.xpath('./td[1]/a/text()').extract_first()
        item['AQI'] = tr.xpath('./td[2]/text()').extract_first()
        item['range'] = tr.xpath('./td[3]/text()').extract_first()
        item['rank'] = tr.xpath('./td[4]/span/text()').extract_first()
        item['PM2_5'] = tr.xpath('./td[5]/text()').extract_first()
        item['PM10'] = tr.xpath('./td[6]/text()').extract_first()
        item['SO2'] = tr.xpath('./td[7]/text()').extract_first()
        item['CO'] = tr.xpath('./td[8]/text()').extract_first()
        item['NO2'] = tr.xpath('./td[9]/text()').extract_first()
        item['O3'] = tr.xpath('./td[last()]/text()').extract_first()
        yield item


def parse_day_data(page_source, city_name):
    selector = Selector(text=page_source)
    trs = selector.xpath('//div[@class="container"]//tbody/tr')[1:]
    for tr in trs:
        item = {}
        item['city'] = city_name
        item['date'] = tr.xpath('./td[1]/text()').extract_first()
        item['AQI'] = tr.xpath('./td[2]/text()').extract_first()
        item['rank'] = tr.xpath('./td[3]/span/text()').extract_first()
        item['PM2_5'] = tr.xpath('./td[4]/text()').extract_first()
        item['PM10'] = tr.xpath('./td[5]/text()').extract_first()
        item['SO2'] = tr.xpath('./td[6]/text()').extract_first()
        item['CO'] = tr.xpath('./td[7]/text()').extract_first()
        item['NO2'] = tr.xpath('./td[8]/text()').extract_first()
        item['O3'] = tr.xpath('./td[last()]/text()').extract_first()
        yield item

def get_month_url_list(page_source):
    selector = Selector(text=page_source)
    return [urljoin(base_url, item) for item in selector.xpath('//div[@class="container"]//tbody/tr/td[1]/a/@href').extract()]


def save_to_mongo(item):
    coll.insert(item)


if __name__ == '__main__':
    city_list = get_city_list()
    for city in city_list:
        city_name = city.split('=')[1]
        page_source = get_city_page_source(city)
        for item in get_month_url_list(page_source):
            day_page_source = get_city_page_source(item)
            for data in parse_day_data(day_page_source, city_name):
                print(data)
                save_to_mongo(data)
