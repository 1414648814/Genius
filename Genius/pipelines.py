# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo, codecs, json
from scrapy.exceptions import DropItem
from pymongo import MongoClient


# 将爬虫内容添加到json文件中
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = codecs.open('CNBLOG.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class GECnBlogUserPipeline(object):
    MONGODB_SERVER = 'localserver'
    MONGODB_PORT = 27017
    MONGODB_DB = 'single_cnblogs'

    def __init__(self):
        try:
            self.client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
            self.db = self.client[self.MONGODB_DB]
        except Exception as e:
            print("Exception:%s"%str(e))

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('SINGLE_MONGODB_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('SINGLE_MONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SINGLE_MONGODB_DB', 'single_cnblogs')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        user_detail = {
            'name' : item.get('name'),
            'link' : item.get('link')
        }
        result = self.db['users'].insert(user_detail)
        item['user_id'] = str(result)
        print(item)
        return item


class GEDuplicateUserPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_time(self, item, spider):
        if item['user_id'] in self.ids_seen:
            raise DropItem('Duplicate item name%s'%item)
        else:
            self.ids_seen.add(item)