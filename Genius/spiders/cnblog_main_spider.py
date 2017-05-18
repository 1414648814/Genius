#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Genius.utils.select_result import list_first_item, strip_null, deduplication, clean_url, getPageList
from Genius.items import GECnMainBlogPost
from Genius.settings import CNBOLG_COOKIE, CNBLOG_MAIN_POST_PAYLOAD, CNBLOG_MAIN_POST_HEADERS


class GECnBlogMainPostSpider(CrawlSpider):
    name = "GECnBlogMainPostSpider"
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        'http://www.cnblogs.com'
    ]

    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        selector = Selector(response)
        for subselector in selector.xpath('//div[@class="post_item"]'):
            post = GECnMainBlogPost()
            post["recommend_num"] = list_first_item(subselector.css('span.diggnum').xpath('text()').extract())
            post["title"] = list_first_item(subselector.css('a.titlelnk').xpath('text()').extract())
            post["post_link"] = list_first_item(subselector.css('a.titlelnk').xpath('@href').extract())
            summary_content = subselector.css('p.post_item_summary').xpath('text()').extract()
            if len(summary_content) > 1:
                summary = summary_content[1]
            else :
                summary = summary_content[0]
            post["brief"] = summary.strip()[:-4]
            footer = subselector.css('div.post_item_foot')
            post["username"] = list_first_item(footer.css('a.lightblue').xpath('text()').extract())
            post["user_link"] = list_first_item(footer.css('a.lightblue').xpath('@href').extract())
            post["time"] = footer.xpath('text()').extract()[1].strip()[4:]
            post["comment_num"] = int(list_first_item(footer.css('span.article_comment a').xpath('text()').extract()).strip()[3:-1])
            post["view_num"] = int(list_first_item(footer.css('span.article_view a').xpath('text()').extract()).strip()[3:-1])
            # if post["post_link"]:
            #     yield Request(url=post["post_link"], callback=self.parse_detail)
            yield post

        page_selector = selector.xpath('//div[@id="pager_bottom"]/div[@id="paging_block"]/div[@class="pager"]')
        next_page_href = str(page_selector.xpath('a/@href').extract()[-1].split('/')[-1])
        next_page_text = page_selector.xpath('a/text()').extract()[-1][:-2]

        if next_page_text == 'Next':
            next_link = ('\?CategoryId=808&CategoryType=%22SiteHome%22&ItemListActionName=%22PostList%22' \
                         'PageIndex=' + next_page_href + '&ParentCategoryId=0').encode(response.encoding)
            next_link = clean_url(response.url, next_link, response.encoding)
            yield Request(url=next_link, callback=self.parse, cookies=CNBOLG_COOKIE, headers=CNBLOG_MAIN_POST_HEADERS,
                          body=json.dumps(getPageList(CNBLOG_MAIN_POST_PAYLOAD, next_page_href)))

    # 获取文章具体的内容，但是没什么必要
    def parse_detail(self, response):
        response_selector = Selector(response)
        yield list_first_item(response_selector.xpath(u'//div[@id="cnblogs_post_body"]').extract())