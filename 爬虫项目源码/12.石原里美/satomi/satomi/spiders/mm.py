# -*- coding: utf-8 -*-
import scrapy
from satomi.items import SatomiItem


class MmSpider(scrapy.Spider):
    name = 'mm'
    allowed_domains = ['movie.douban.com/celebrity/1016930/photos']
    start_urls = ['https://movie.douban.com/celebrity/1016930/photos/?start={number}'.format(number=str(i*30)) for i in range(11)]

    def parse(self, response):
        item = SatomiItem()
        item['image_urls'] = response.xpath('//div[@class="cover"]/a/img/@src').extract()
        yield item

