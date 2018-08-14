# -*- coding: utf-8 -*-
import scrapy
from onepiece.items import OnepieceItem


class OnePieceComicSpider(scrapy.Spider):
    name = 'one_piece_comic'
    allowed_domains = ['one-piece.cn']
    offset = 10801
    url = "https://one-piece.cn/post/"
    start_urls = [url + str(offset)]

    def parse(self, response):
        #  返回从json里获取data段的数据集
        data = response.xpath('//*[@id="contents"]/article/div/div[1]/p/img')
        data.pop()

        for i, each in enumerate(data):
            each_name = each.xpath('@alt').extract()[0]
            each_url = each.xpath('@src').extract()[0]

            item = OnepieceItem()
            item['name'] = each_name
            item['imagesName'] = "%s.jpg" % (i + 1)
            item['imagesUrls'] = each_url
            yield item

        self.offset += 1

        # yield scrapy.Request(self.url + str(self.offset), callback=self.parse, dont_filter=True)
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
