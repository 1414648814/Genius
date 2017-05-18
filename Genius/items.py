# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


# 博客园主界面文章
class GECnMainBlogPost(Item):
    post_id = Field()
    title = Field()  # 文章名称
    post_link = Field()  # 文章连接
    username = Field()  # 用户名字
    user_link = Field()  # 用户链接
    brief = Field()  # 文章简介
    time = Field()  # 发布时间
    recommend_num = Field()  # 评论数量
    view_num = Field()  # 阅读人数
    comment_num = Field()  # 评论数量

    def detail(self):
        print("title:" + str(self.title.values()) + "\nauthor" + str(self.username.values()))


# 博客园博主文章
class GECnUserBlogPost(Item):
    post_id = Field()
    title = Field()  # 文章名称
    post_link = Field()  # 文章连接
    username = Field()  # 用户名字
    brief = Field()  # 文章简介
    time = Field()  # 发布时间
    view_num = Field()  # 阅读人数
    comment_num = Field()  # 评论数量

    def detail(self):
        print("title:" + str(self.title.values()) + "\nauthor" + str(self.username.values()))


# 博客园用户数据
class GECnBlogUser(Item):
    user_id = Field()  # 用户id，用来去重
    name = Field()  # 姓名
    link = Field()  # 博客网址
    icon = Field()  # 头像
    sex = Field()  # 性别
    birthday = Field()  # 出生日期
    ranking = Field()  # 排名
    score = Field()  # 积分
    rss_url = Field()  # rss网址
    post_num = Field()  # 文章个数
    last_post_time = Field()  # 最近一次更新的时间
    hometown = Field()  # 出生地
    residence = Field() # 现在居住地
    work_condition = Field()  # 工作状况
    work_position = Field()  # 工作职位
    work_unit = Field()  # 工作单位
    marriage = Field()  # 结婚状况
    interest = Field()  # 感兴趣的技术
    goal = Field()  # 目标
    motto = Field()  # 座右铭
    intro = Field()  # 自我介绍
    qq = Field()  # qq
    use_time = Field()  # 园龄
    follow_num = Field()  # 关注人数
    fans_num = Field()  # 粉丝人数

    def detail(self):
        print('name:' + str(self.name.values()) + '\nlink' + str(self.link.values()))


# 博客园用户动态
class GECnBlogUserActivity(Item):
    activity_id = Field()
    name = Field()
    type = Field()
    event = Field()
    desc = Field()
    time = Field()

    def detail(self):
        print('name:' + str(self.name.values()) + '\nevent' + str(self.event.values()))


# 博客园用户为解决的提问
class GECnBlogQuestion(Item):
    question_id = Field()
    title = Field()
    title_link = Field()
    desc = Field()
    score = Field()
    username = Field()
    view_num = Field()
    reply_num = Field()
    time = Field()
    tag = Field()  # 以字符串中间|进行存储

    def detail(self):
        print('username' + str(self.username.values()) + "\n" + str(self.title.values()))


# 博客园主页新闻文章
class GECnBlogMainNewsPost(GECnMainBlogPost):
    tag = Field()
    tag_link = Field()