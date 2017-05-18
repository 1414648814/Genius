#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Genius.utils.select_result import list_first_str, list_first_int, list_first_item, strip_null, deduplication, clean_url
from Genius.items import GECnBlogQuestion
from Genius.settings import CNBOLG_COOKIE, CNBLOG_MAIN_POST_HEADERS, CNBLOG_QUESTION_URL


class GECnBlogQuestionSpider(CrawlSpider):
    name = "GECnBlogQuestionSpider"
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        'https://q.cnblogs.com/list/unsolved?page=1'
    ]

    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        selector = Selector(response)
        for subselector in selector.xpath('//div[@class="one_entity"]'):
            question = GECnBlogQuestion()
            question["reply_num"] = list_first_int(subselector.xpath('div[1]/div/div[1]/text()').extract())
            item_selector = subselector.xpath('div[2]')
            if list_first_item(item_selector.xpath('h2/span').extract()) is not None:
                question["score"] = list_first_int(item_selector.xpath('h2/span/text()').extract())
            else:
                question["score"] = 0
            question["title"] = list_first_str(item_selector.xpath('h2/a/text()').extract())
            question["title_link"] = CNBLOG_QUESTION_URL + \
                                 list_first_str(item_selector.xpath('h2/a/@href').extract())
            question["desc"] = list_first_str(item_selector.xpath('div[@class="news_summary"]/text()').extract())
            item_footer_selector = item_selector.xpath('div[@class="news_footer"]')
            question["username"] = list_first_str(item_footer_selector.xpath('div[2]/a[2]/text()').extract())
            question["view_num"] = list_first_int(item_footer_selector.xpath('div[2]/text()').extract())[3:-1]
            question["time"] = list_first_str(item_footer_selector.xpath('div[2]/span/text()').extract())
            tag_str = ''
            for i, tag_selector in enumerate(item_footer_selector.xpath('div[1]/a')):
                tag_str += list_first_str(tag_selector.xpath('text()').extract()) + '|'
            question['tag'] = tag_str
            yield question

        page_selector = selector.xpath('//div[@id="pager"]')
        next_page_href = str(page_selector.xpath('a/@href').extract()[-1].split('/')[-1])
        next_page_text = page_selector.xpath('a/text()').extract()[-1][:-2]

        if next_page_text == 'Next':
            yield Request(url=CNBLOG_QUESTION_URL + next_page_href, callback=self.parse, cookies=CNBOLG_COOKIE, headers=CNBLOG_MAIN_POST_HEADERS)