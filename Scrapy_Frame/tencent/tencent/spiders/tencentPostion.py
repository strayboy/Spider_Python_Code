# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencentpostionSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']

    url = 'http://hr.tencent.com/position.php?&start='
    offset = 0

    start_urls = [url + str(offset)]




    def parse(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            # 初始化模型对象
            item = TencentItem()
            try:
                # 职位名称
                if each.xpath("./td[1]/a/text()").extract()[0] == '':
                    item['positionName'] = ''
                else:
                    item['positionName'] = each.xpath("./td[1]/a/text()").extract()[0]
                # 详情链接
                if each.xpath("./td[1]/a/@href").extract()[0] == '':
                    item['positonLink'] = ''
                else:
                    item['positonLink'] = each.xpath("./td[1]/a/@href").extract()[0]
                # 职位类别
                if each.xpath("./td[2]/text()").extract()[0] == '':
                    item['positionType'] = ''
                else:
                    item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
                # 招聘人数
                if each.xpath("./td[3]/text()").extract()[0] == '':
                    item['peopleNum'] = ''
                else:
                    item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
                # 工作地点
                if each.xpath("./td[4]/text()").extract()[0] == '':
                    item['workLocation'] = ''
                else:
                    item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
                # 发布时间
                if each.xpath("./td[5]/text()").extract()[0] == '':
                    item['publisTime'] = ''
                else:
                    item['publisTime'] = each.xpath("./td[5]/text()").extract()[0]
            except Exception as e:
                pass

            yield item

        if self.offset < 2100:
            self.offset += 10
        # else:
        #     raise "结束工作"

        # 每次处理完一页的数据后，重新发送下一页面请求
        # self.offset自增10，同时拼为新的URL，并调用回调函数self.parse处理Response
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)


