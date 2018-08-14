# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline, DropItem
from scrapy.utils.project import get_project_settings


class OnePieceImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_url = item["imagesUrls"]
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 固定写法，获取图片路径，同时判断这个路径是否正确，如果正确，就放到 image_path里，ImagesPipeline源码剖析可见
        image_path = [x["path"] for ok, x in results if ok]
        folder_name = item['name'][:9]
        image_uid = item['imagesName']
        cur_dir = os.listdir(self.IMAGES_STORE)
        if folder_name not in cur_dir:
            os.mkdir(self.IMAGES_STORE + "/" + folder_name)
        os.rename(self.IMAGES_STORE + "/" + image_path[0],
                  self.IMAGES_STORE + "/" + folder_name + '/' + image_uid)
        if not image_path:
            raise DropItem('Item contains no images')
        item["imagesPath"] = self.IMAGES_STORE + "/" + item["name"]

        return item
