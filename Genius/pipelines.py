# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo, codecs, json
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from .settings import SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT, SINGLE_MONGODB_DB


# 将爬虫内容添加到json文件中，这里也要可以进行区分，不用把所有的数据都存进一个json文件
class JsonWriterPipeline(object):
    def __init__(self):
        self.main_post_file = codecs.open('main_post.json', 'w', encoding='utf-8')
        self.user_post_file = codecs.open('user_post.json', 'w', encoding='utf-8')
        self.user_detail_file = codecs.open('user_detail.json', 'w', encoding='utf-8')
        self.user_activity_file = codecs.open('user_activity.json', 'w', encoding='utf-8')
        self.question_file = codecs.open('question.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if spider.name == 'GECnBlogPopularUserSpider':
            if item['activity_id'] is not None:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.user_activity_file.write(line)
            elif item['post_id'] is not None:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.user_post_file.write(line)
            else:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.user_detail_file.write(line)
        elif spider.name == 'GECnBlogMainPostSpider':
            self.main_post_file.close()
        elif spider.name == 'GECnBlogQuestionSpider':
            self.question_file.close()
        return item

    def spider_closed(self, spider):
        if spider.name == 'GECnBlogPopularUserSpider':
            self.user_post_file.close()
            self.user_detail_file.close()
            self.user_activity_file.close()
        elif spider.name == 'GECnBlogMainPostSpider':
            self.main_post_file.close()
        elif spider.name == 'GECnBlogQuestionSpider':
            self.question_file.close()


class GECnBlog(object):
    def __init__(self):
        try:
            self.client = MongoClient(SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT)
            self.db = self.client[SINGLE_MONGODB_DB]
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
        if spider.name == 'GECnBlogPopularUserSpider':
            return GECnBlogUserPipeline.process_item(self.db, item, spider)
        elif spider.name == 'GECnBlogMainPostSpider':
            return GECnBlogMainPostPipeline.process_item(self.db, item, spider)
        elif spider.name == 'GECnBlogQuestionSpider':
            return GECnBlogQuestionPipeline.process_item(self.db, item, spider)


class GECnBlogUserPipeline(object):
    @staticmethod
    def process_item(db, item, spider):
        # 区分博主信息和文章信息和活动信息
        if item['activity_id'] is not None:
            user_detail = {
                'name' : item.get('name'),
                'type' : item.get('type'),
                'event' : item.get('event'),
                'desc' : item.get('desc'),
                'time' : item.get('time'),
            }
            result = db['activities'].insert(user_detail)
            item['activity_id'] = str(result)
        elif item['post_id'] is not None:
            user_detail = {
                'title': item.get('title'),
                'post_link': item.get('post_link'),
                'username': item.get('username'),
                'brief': item.get('brief'),
                'time': item.get('time'),
                'view_num': item.get('view_num'),
                'comment_num': item.get('comment_num')
            }
            result = db['posts'].insert(user_detail)
            item['post_id'] = str(result)
        else :  # 默认是用户信息
            user_detail = {
                'name': item.get('name'),
                'link': item.get('link'),
                'icon': item.get('icon'),
                'sex': item.get('sex') or '',
                'birthday': item.get('birthday') or '',
                'ranking': item.get('ranking') or 0,
                'score': item.get('score') or 0,
                'rss_url': item.get('rss_url') or '',
                'post_num': item.get('post_num') or 0,
                'last_post_time': item.get('last_post_time') or '',
                'hometown': item.get('hometown') or '',
                'residence': item.get('residence') or '',
                'work_condition': item.get('work_condition') or '',
                'work_position': item.get('work_position') or '',
                'work_unit': item.get('work_unit') or '',
                'marriage': item.get('marriage') or '',
                'interest': item.get('interest') or '',
                'goal': item.get('goal') or '',
                'motto': item.get('motto') or '',
                'intro': item.get('intro') or '',
                'qq': item.get('link') or '',
                'use_time': item.get('use_time') or '',
                'follow_num': item.get('follow_num') or 0,
                'fans_num': item.get('fans_num') or 0
            }
            result = db['users'].insert(user_detail)
            item['user_id'] = str(result)
        return item


class GECnBlogMainPostPipeline(object):
    @staticmethod
    def process_item(db, item, spider):
        post_detail = {
            'title': item.get('title'),
            'post_link': item.get('post_link'),
            'username': item.get('username'),
            'user_link': item.get('user_link'),
            'brief': item.get('brief'),
            'time': item.get('time'),
            'recommend_num': item.get('recommend_num'),
            'view_num': item.get('view_num'),
            'comment_num': item.get('comment_num')
        }
        result = db['main_post'].insert(post_detail)
        item['post_id'] = str(result)
        return item


class GECnBlogQuestionPipeline(object):
    @staticmethod
    def process_item(db, item, spider):
        question_detail = {

        }
        result = db['questions'].insert(question_detail)
        item['question_id'] = str(result)
        return item


# 去重问题暂时放一放
class GEDuplicatePipeline(object):
    def __init__(self):
        self.ids_seen = set()  # 这里可能会有问题

    def process_time(self, item, spider):
        if item['user_id'] in self.ids_seen:
            raise DropItem('Duplicate item name%s'%item)
        else:
            self.ids_seen.add(item)