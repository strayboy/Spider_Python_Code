# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pic177.items import Pic177Item


class Pic177InfoSpider(CrawlSpider):
    name = 'pic177_info'
    allowed_domains = ['177piczz.info']
    url = "http://www.177piczz.info/html/category/tt/page/1"
    start_urls = [url]

    page_lx = LinkExtractor(allow='category/tt/page/\d+')
    rules = [
        Rule(page_lx, callback="parseHome", follow=True)
    ]

    def parseHome(self, response):
        # 打开主页
        for each in response.xpath('//div/h2'):
            comic_url = each.xpath('./a/@href').extract()
            title = each.xpath('./a/text()').extract()
            item_home = {}
            item_home['file_name'] = title[0]
            item_home['file_url'] = comic_url[0]
            offset = 1
            url_entry = comic_url[0] + '/' + str(offset)
            yield Request(url=url_entry, meta={'item_temp': item_home}, callback=self.parseComic)

    def parseComic(self, response):
        # 进入一个页面（一个漫画共有多少页面），判定多少页面,生成一个列表
        item2 = response.meta['item_temp']
        url_li = response.xpath('//*[@id="single-navi"]/div/p/a/@href').extract()
        url_li.pop()
        url_first = item2['file_url']
        url_li = [url_first] + url_li
        for i, each in enumerate(url_li):
            yield Request(url=each, meta={'temp': item2, 'index': i + 1}, callback=self.parseComicTwo)

    def parseComicTwo(self, response):

        item3 = response.meta['temp']
        index = response.meta['index']

        data = response.xpath('//div[2]/p/img')
        for i, each in enumerate(data):
            item = Pic177Item()
            item['file_name'] = item3['file_name']
            item['file_url'] = item3['file_url']
            item['image_name'] = "%s.jpg" % (str(index)+'_'+str(i))
            item['image_url'] = each.xpath('./@src').extract()[0]
            yield item
