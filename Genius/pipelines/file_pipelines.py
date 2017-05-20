import codecs, json, scrapy, pymongo, os, logging
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from ..utils.select_result import list_first_item, list_first_str
from pymongo import MongoClient
from Genius.settings import SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT, SINGLE_MONGODB_DB
from Genius.utils.select_result import get_linkmd5id


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
            if hasattr(item, 'activity_id'):
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.user_activity_file.write(line)
            elif hasattr(item, 'post_id'):
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.user_post_file.write(line)
            else:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.user_detail_file.write(line)
        elif spider.name == 'GECnBlogMainPostSpider':
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.main_post_file.write(line)
        elif spider.name == 'GECnBlogQuestionSpider':
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.question_file.write(line)
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


# 博客园用户头像
class GECNBLOGUserCoverImage(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        try:
            self.client = MongoClient(SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT)
            self.db = self.client[SINGLE_MONGODB_DB]
            self.images_store = store_uri
        except Exception as e:
            print("Exception:%s"%str(e))
        super(GECNBLOGUserCoverImage, self).__init__(store_uri, download_func, settings)

    # 可能会有多个item
    def get_media_requests(self, item, info):
        if item is None:
            logging.warning('GECNBLOGUserCoverImage: item is None')
            return
        if 'icon' in item.keys():
            yield Request(item['icon'])

    def item_completed(self, results, item, info):
        if item is None:
            return
        if 'icon' in item.keys():
            image_paths = [x['path'] for ok, x in results if ok]
            if list_first_item(image_paths) is None:
                item['icon_path'] = ''
                raise DropItem("Item contains no images")
            linkmd5id = get_linkmd5id(item['link'])
            user = self.db['users'].find_one({"user_id": linkmd5id})
            if user is not None:
                icon_path = list_first_str(image_paths)
                item['icon_path'] = os.path.join(os.path.abspath(self.images_store), icon_path) if icon_path else ""
                self.db['users'].update_one(
                    {"user_id": linkmd5id},
                    {'$set': {'icon_path': item['icon_path']}},
                    True
                )
                logging.info('GECNBLOGUserCoverImage: item is updated successfully')
                # 可以将图片的路径加入到数据库中
                return item