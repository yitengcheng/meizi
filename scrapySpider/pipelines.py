# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exporters import JsonItemExporter
from pathlib import Path
import os
import requests
import uuid
from scrapySpider.settings import USER_AGENT, IMAGES_STORE
import re


class ScrapyspiderPipeline(object):

    def process_item(self, item, spider):
        return item


class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('item.json', 'wb')
        self.exporter = JsonItemExporter(
            self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        headers = {'User-Agent': USER_AGENT, 'Referer': 'http://www.baidu.com/'}
        res = re.match(r'(.+)（\d+）', item['title'][0])
        if res:
            title = res.group(1)
        else:
            title = item['title'][0]
        img_urls = item['img_url']
        file_path = IMAGES_STORE + '/' + title
        my_file = Path(file_path)
        img_name = uuid.uuid1()
        wb_path = '{0}/{1}.jpg'
        if not my_file.exists():
            os.makedirs(my_file)
        for img_url in img_urls:
            response = requests.get(img_url, headers=headers)
            with open(wb_path.format(file_path, img_name), 'wb') as fd:
                for chunk in response.iter_content(128):
                    fd.write(chunk)
