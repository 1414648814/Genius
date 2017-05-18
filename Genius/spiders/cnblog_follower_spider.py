#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import scrapy_splash, scrapy
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor as extractor
from Genius.settings import CNBOLG_COOKIE, CNBLOG_USER_FOLLOWER_HEADERS, CNBLOG_USER_FOLLOWER_URL, CNBLOG_USER_HOME_URL
from Genius.utils.select_result import list_first_item, strip_null, deduplication, clean_url

class GECnBlogFollowerSpider(CrawlSpider):
    #定义爬虫的名称
    name = "GECnBlogFollowerSpider"
    #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
    allowed_domains = ["cnblogs.com"]
    users = []

    # 重写启动函数
    def start_requests(self):
        yield SplashRequest(url="https://home.cnblogs.com/u/George1994/followees/", callback=self.parse_follower_item,
            args={
                # optional; parameters passed to Splash HTTP API
                'wait': 0.5,
                "cookies": CNBOLG_COOKIE,
                "headers": CNBLOG_USER_FOLLOWER_HEADERS,
                # 'url' is prefilled from request url
                # 'http_method' is set to 'POST' for POST requests
                # 'body' is set to request body for POST requests
            },
            endpoint='render.json',  # optional; default is render.html
            # splash_url='<url>',  # optional; overrides SPLASH_URL
            slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
        )

    # 解析用户数据
    def parse_user_item(self, response):
        print("user")
        # "https://home.cnblogs.com/u/George1994/followers?groupId=%2200000000-0000-0000-0000-000000000000%22&isFollowes=false&page=1&uid=%2270641f56-277a-e611-9fc1-ac853d9f53cc%22"

    # 解析用户关注数据
    def parse_follower_item(self, response):
        print("follower")
        selector = Selector(response)
        for subselector in selector:
            print(subselector.xpath('//div[@class="avatar_name"]'))
            print(subselector.extract())

            user_url = list_first_item(subselector.css('div.avatar_name a').xpath('@href'))
            if user_url:
                user_url = user_url.encode(response.encoding)
                user_url = clean_url(response.url, user_url, response.encoding)
                print(user_url)

    # 解析用户粉丝数据
    def parse_fans_item(self, response):
        print("fans")