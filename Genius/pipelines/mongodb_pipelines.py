# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo, logging
from pymongo import MongoClient
from Genius.settings import SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT, SINGLE_MONGODB_DB
from Genius.utils.select_result import get_linkmd5id


class GECnBlogPipeline(object):
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
        if 'activity_id' in item.keys():
            activity_detail = {
                'activity_id' : item.get('activity_id'),
                'name' : item.get('name'),
                'type' : item.get('type'),
                'event' : item.get('event'),
                'event_url' : item.get('event_url'),
                'desc' : item.get('desc'),
                'time' : item.get('time'),
            }
            result = db['activities'].insert(activity_detail)
            item['mongodb_id'] = str(result)
            logging.info('GECnBlogUserPipeline: item is added successfully')
            return item
        elif 'post_id' in item.keys():
            post_detail = {
                'post_id' : item.get('post_id'),
                'title': item.get('title'),
                'post_link': item.get('post_link'),
                'username': item.get('username'),
                'user_url' : item.get('user_url'),
                'brief': item.get('brief'),
                'time': item.get('time'),
                'view_num': item.get('view_num'),
                'comment_num': item.get('comment_num')
            }
            result = db['user_post'].insert(post_detail)
            item['mongodb_id'] = str(result)
            logging.info('GECnBlogUserPipeline: item is added successfully')
            return item
        elif 'user_id' in item.keys():  # 默认是用户信息
            linkmd5id = get_linkmd5id(item['link'])
            user = db['users'].find_one({"user_id": linkmd5id})
            if user is None:
                user_detail = {
                    'user_id' : item.get('user_id'),
                    'nickname': item.get('nickname'),
                    'name': item.get('name', ''),
                    'link': item.get('link'),
                    'icon': item.get('icon', ''),
                    'sex': item.get('sex', ''),
                    'birthday': item.get('birthday', ''),
                    'ranking': item.get('ranking', 0),
                    'score': item.get('score', 0),
                    'rss_url': item.get('rss_url', ''),
                    'post_num': item.get('post_num', 0),
                    'last_post_time': item.get('last_post_time', ''),
                    'hometown': item.get('hometown', ''),
                    'residence': item.get('residence', ''),
                    'work_condition': item.get('work_condition', ''),
                    'work_position': item.get('work_position', ''),
                    'work_unit': item.get('work_unit', ''),
                    'marriage': item.get('marriage', ''),
                    'interest': item.get('interest', ''),
                    'goal': item.get('goal', ''),
                    'motto': item.get('motto', ''),
                    'intro': item.get('intro', ''),
                    'qq': item.get('qq', ''),
                    'use_time': item.get('use_time', ''),
                    'follow_num': item.get('follow_num', 0),
                    'fans_num': item.get('fans_num', 0)
                }
                result = db['users'].insert_one(user_detail)
                item['mongodb_id'] = str(result)  # 并不需要将其存到数据库中
                logging.info('GECnBlogUserPipeline: item is added successfully')
                return item
            else:
                for key in item.keys():
                    if item[key] != user[key] and item[key] != 0 and item[key] != '' and key != 'mongodb_id':
                        db['users'].update_one(
                            {"user_id": linkmd5id},
                            {'$set': {key: item[key]}}
                        )
                logging.info('GECnBlogUserPipeline: item is updated successfully')
                return db['users'].find_one({"user_id": linkmd5id})


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
        item['mongodb_id'] = str(result)
        logging.info('GECnBlogMainPostPipeline: item is add successfully')
        return item


class GECnBlogQuestionPipeline(object):
    @staticmethod
    def process_item(db, item, spider):
        question_detail = {
            'title': item.get('title'),
            'title_link': item.get('title_link'),
            'desc': item.get('desc'),
            'score': item.get('score'),
            'username': item.get('username'),
            'view_num': item.get('view_num'),
            'reply_num': item.get('reply_num'),
            'time': item.get('time'),
            'tag': item.get('tag')
        }
        result = db['questions'].insert(question_detail)
        item['mongodb_id'] = str(result)
        logging.info('GECnBlogQuestionPipeline: item is add successfully')
        return item