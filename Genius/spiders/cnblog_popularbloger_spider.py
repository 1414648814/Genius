from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as extractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from Genius.utils.select_result import list_first_item, strip_null, deduplication, clean_url, getPageList
from Genius.settings import CNBLOG_POPULAR_URL, CNBLOG_MAIN_POST_HEADERS, CNBOLG_COOKIE, CNBLOG_USER_HOME_URL
from Genius.items import GECnBlogUser, GECnBlogUserActivity


class GECnBlogPopularUserSpider(CrawlSpider):
    #定义爬虫的名称
    name = "GECnBlogPopularUserSpider"
    #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
    allowed_domains = ["cnblogs.com"]
    #定义抓取的入口url
    start_urls = [
        CNBLOG_POPULAR_URL
    ]

    def parse(self, response):
        selector = Selector(response).xpath('//td')
        user = GECnBlogUser()
        for index, subselector in enumerate(selector):
            ranking = list_first_item(subselector.xpath("string(//small[1]/text())").extract()).strip()[:-1]
            content = list_first_item(subselector.xpath("string(//small[2]/text())").extract()).strip()[1:-1].split(',')
            post_num, last_post_time, score = content[0].strip(), content[1].strip(), content[2].strip()
            link = list_first_item(subselector.xpath("string(//a[1]/@href)").extract()).strip()
            name = list_first_item(subselector.xpath("string(//a[1]/text())").extract()).strip()
            rss_url = list_first_item(subselector.xpath("string(//a[2]/@href)").extract()).strip()
            user['name'], user['link'], user['ranking'], user['score'], user['rss_url'] = name, link, ranking, score, rss_url
            user['post_num'], user['last_post_time'] = post_num, last_post_time
            if link is not None:
                yield Request(url=link, callback=self.parse_user, headers=CNBLOG_MAIN_POST_HEADERS)
        # test
        # detail_url = 'https://home.cnblogs.com/u/huangxincheng'
        # yield Request(url=detail_url, callback=self.parse_user_detail, headers=CNBLOG_MAIN_POST_HEADERS, cookies=CNBOLG_COOKIE)

    # 爬取用户博文信息
    def parse_user(self, response):
        next_link = (response.url.split('/')[-2]).encode(response.encoding)
        detail_url = clean_url('https://home.cnblogs.com/u/', next_link, response.encoding)
        yield Request(url=detail_url, callback=self.parse_user_detail, headers=CNBLOG_MAIN_POST_HEADERS, cookies=CNBOLG_COOKIE)

    # 爬取用户具体信息
    def parse_user_detail(self, response):
        user = GECnBlogUser()
        selector = Selector(response)
        follow_count = list_first_item(selector.xpath('//a[@id="following_count"]/text()').extract()).strip()
        fans_count = list_first_item(selector.xpath('//a[@id="follower_count"]/text()').extract()).strip()
        icon = list_first_item(selector.xpath('//img[@class="img_avatar"]/@src').extract()).strip()
        user['follow_num'], user['fans_num'], user['icon'] = follow_count, fans_count, icon
        li_selector = selector.xpath('//ul[@class="user_profile"]//li')
        for i, subselector in enumerate(li_selector):
            if i == 0:
                continue
            key = list_first_item(subselector.css('span::text').extract()).strip()[:-1]
            if key == "园龄":
                use_time = list_first_item(subselector.xpath('string(//span[2]/text())').extract()).strip()
                user['use_time'] = use_time
            elif key == "博客":
                link = list_first_item(subselector.xpath('a/@href').extract()).strip()
                user['link'] = link
            elif key == '姓名':
                name = list_first_item(subselector.xpath('text()').extract()).strip()
                user['name'] = name
            elif key == '家乡':
                hometown = list_first_item(subselector.xpath('text()').extract()).strip()
                user['hometown'] = hometown
            elif key == '现居住地':
                residence = list_first_item(subselector.xpath('text()').extract()).strip()
                user['residence'] = residence
            elif key == '座右铭':
                motto = list_first_item(subselector.xpath('text()').extract()).strip()
                user['motto'] = motto
            elif key == '自我介绍':
                intro = list_first_item(subselector.xpath('text()').extract()).strip()
                user['intro'] = intro
            elif key == '婚姻':
                marriage = list_first_item(subselector.xpath('text()').extract()).strip()
                user['marriage'] = marriage
            elif key == '工作状况':
                work_condition = list_first_item(subselector.xpath('text()').extract()).strip()
                user['work_condition'] = work_condition
            elif key == '感兴趣的技术':
                interest = list_first_item(subselector.xpath('text()').extract()).strip()
                user['interest'] = interest
            elif key == '最近目标':
                goal = list_first_item(subselector.xpath('text()').extract()).strip()
                user['goal'] = goal
            elif key == 'QQ':
                qq = list_first_item(subselector.xpath('text()').extract()).strip()
                user['qq'] = qq
            elif key == '职位':
                work_position = list_first_item(subselector.xpath('text()').extract()).strip()
                user['work_position'] = work_position
            elif key == '单位':
                work_unit = list_first_item(subselector.xpath('text()').extract()).strip()
                user['work_unit'] = work_unit
            elif key == '出生日期':
                birthday = list_first_item(subselector.xpath('text()').extract()).strip()
                user['birthday'] = birthday

        yield user
        next_link = (user['link'].split('/')[-2] + "/feed/1.html").encode(response.encoding)
        activity_url = clean_url(response.url, next_link, response.encoding)
        yield Request(url=activity_url, callback=self.prase_activity, headers=CNBLOG_MAIN_POST_HEADERS, cookies=CNBOLG_COOKIE)

    # 爬取活动信息
    def prase_activity(self, response):
        selector = Selector(response)
        item_selector = selector.xpath('//ul[@id="feed_list"]').css('li.feed_item')
        for i, subselector in enumerate(item_selector):
            activity = GECnBlogUserActivity()
            title_selector = subselector.xpath('div/div[@class="feed_title"]')
            name = list_first_item(title_selector.xpath('string(a[1]/text())').extract()).strip()
            type = list_first_item(title_selector.xpath('text()').extract()).strip()[:-1]
            event = list_first_item(title_selector.xpath('string(a[2]/text())').extract()).strip()
            activity['name'] = name
            if type == '评论博客' or type == '发表博客':
                time = list_first_item(title_selector.xpath('span/text()').extract()).strip()
                activity['type'], activity['event'], activity['time'] = type, event, time
                desc = list_first_item(subselector.xpath('div/div[@class="feed_desc"]/text()').extract()).strip()
                activity["desc"] = desc
            else:
                activity['type'], activity['event'], activity['time'], activity['desc'] = "话题", event, event, event
            yield activity

        next_selector = selector.xpath('//div[@class="block_arrow"]/a')
        pager_selector = selector.xpath('//div[@class="block_arrow"]/div[@class="pager"]')
        if list_first_item(next_selector.extract()) is not None:
            nexturl = list_first_item(next_selector.xpath('@href').extract()).strip()
            nexturl = CNBLOG_USER_HOME_URL + nexturl
            yield Request(url=nexturl, callback=self.prase_activity, headers=CNBLOG_MAIN_POST_HEADERS,
                          cookies=CNBOLG_COOKIE)
        elif list_first_item(pager_selector.extract()) is not None:
            next_page_href = str(pager_selector.xpath('a/@href').extract()[-1])
            next_page_text = pager_selector.xpath('a/text()').extract()[-1][:-2]
            if next_page_text == 'Next':
                next_link = CNBLOG_USER_HOME_URL + next_page_href
                yield Request(url=next_link, callback=self.prase_activity, cookies=CNBOLG_COOKIE,
                              headers=CNBLOG_MAIN_POST_HEADERS)

