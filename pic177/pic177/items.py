# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Pic177Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_name = scrapy.Field()  # 文件夹名字
    file_url = scrapy.Field()  #  comic的URL,漫画入口
    image_name = scrapy.Field()  # 存储图片的名字
    image_url = scrapy.Field()  # 图片的url路径
    image_path = scrapy.Field()  # 图片保存在本地的路径
