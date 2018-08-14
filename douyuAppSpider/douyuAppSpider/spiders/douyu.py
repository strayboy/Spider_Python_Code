# -*- coding: utf-8 -*-
import scrapy, json
from douyuAppSpider.items import DouyuappspiderItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ["http://capi.douyucdn.cn"]

    dy_offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    start_urls = [url + str(dy_offset)]

    def parse(self, response):
        #  返回从json里获取data段的数据集
        data = json.loads(response.text)["data"]
        if data == []: return

        for each in data:

            item = DouyuappspiderItem()

            item['name'] = each['nickname']
            item['imagesUrls'] = each['vertical_src']

            yield item

        self.dy_offset += 20

        yield scrapy.Request(self.url + str(self.dy_offset), callback=self.parse,dont_filter=True)
