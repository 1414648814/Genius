# from setuptools import setup, find_packages
#
# setup(name='scrapy-mymodule',
#   entry_points={
#     'scrapy.commands': [
#       'crawlall=cnblogs.commands:crawlall',
#     ],
#   },
#  )

import scrapy, logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Genius.spiders.cnblog_main_spider import GECnBlogMainPostSpider
from Genius.spiders.cnblog_follower_spider import GECnBlogFollowerSpider
from Genius.spiders.cnblog_popularbloger_spider import GECnBlogPopularUserSpider
from Genius.spiders.cnblog_question_spider import GECnBlogQuestionSpider


# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logging/scrapy.log',
                    filemode='w')

process = CrawlerProcess(get_project_settings())

process.crawl(GECnBlogPopularUserSpider)
process.start() # the script will block here until the crawling is finished