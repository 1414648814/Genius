#!/usr/bin/python
#-*- coding:utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as extractor
from ..settings import CNBLOG_USER_URL

class GECnBlogUserPostSpider(CrawlSpider):
    #定义爬虫的名称
    name = "GECnBlogUserPostSpider"
    #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
    allowed_domains = ["cnblogs.com"]
    #定义抓取的入口url
    start_urls = [
        CNBLOG_USER_URL
    ]
    # 定义爬取URL的规则，并指定回调函数为parse_item
    rules = [
        Rule(extractor(allow=(CNBLOG_USER_URL + "/default.html\?page=\d{1,}")), #此处要注意?号的转换，复制过来需要对?号进行转换。
			 follow=True,
			 callback='parse_item')
    ]

    #定义回调函数
    #提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item(self, response):
        print("hahha")