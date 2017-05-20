# -*- coding: utf-8 -*-

# Scrapy settings for Genius project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'Genius'

SPIDER_MODULES = ['Genius.spiders']
NEWSPIDER_MODULE = 'Genius.spiders'

# Project dir
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Genius (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Genius.middlewares.RandomUserAgent': 543, # 设置user-agent
   #  'scrapy_crawlera.CrawleraMiddleware': 600, #crawlera代理用到
    # 支持缓存，避免重复发送浪费流量
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# 数字范围在0到1000之间，存进mongodb
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 200,  # redis保存下item，已经存在的item则丢弃，可以用来查看item
    'Genius.pipelines.mongodb_pipelines.GECnBlogPipeline': 300,
    'Genius.pipelines.file_pipelines.GECNBLOGUserCoverImage': 400,
    # 'Genius.pipelines.pipelines.JsonWriterPipeline': 500
}

# 单mongodb
SINGLE_MONGODB_SERVER = 'localhost'
SINGLE_MONGODB_PORT = 27017
SINGLE_MONGODB_DB = 'single_cnblogs'

# 集群mongodb
SHARED_MONGDB_SERVER = 'localhost'
SHARED_MONGDB_PORT = 27017
SHARED_MONGDB_DB = 'shared_cnblogs'


# redis优先级队列
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 设置一个去重的类，确保爬虫通过redis进行缓存
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

# 不清除Redis队列、这样可以暂停/恢复 爬取
SCHEDULER_PERSIST = True

# 指定排序爬取地址时使用的队列，默认是按照优先级排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# 最大空闲时间防止分布式爬虫因为等待而关闭
SCHEDULER_IDLE_BEFORE_CLOSE = 10

# 指定连接到redis时使用的端口和地址（可选）
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# 可以进行自定义参数
# REDIS_PARAMS = {}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# 开启自动限速的功能
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# 请求目标频率
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.5
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 定制图片
IMAGES_MIN_WIDTH = 50
IMAGES_MIN_HEIGHT = 50
IMAGES_STORE = os.path.join(PROJECT_DIR,'cover_imgae')

# 打印文件
LOG_FILE = 'logging/scrapy.log'

REDIRECT_ENABLED = False  # 禁止过重定向

USER_AGENTS = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

PROXIES = [
    {'ip_port': '111.11.228.75:80', 'user_pass': ''},
    {'ip_port': '120.198.243.22:80', 'user_pass': ''},
    {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
]

CNBOLG_COOKIE = {
    "a3604_times" : r"1",
    "UM_distinctid" : r"15abb61c2d5a53-0ae9bfec54598-1d396850-fa000-15abb61c2d66ae",
    "CNZZDATA3510305" : r"cnzz_eid%3D1100257798-1489202430-http%253A%252F%252Fwww.cnblogs.com%252F%26ntime%3D1489202430",
    "CNZZDATA5475061" : r"cnzz_eid%3D78767875-1489231442-http%253A%252F%252Fwww.cnblogs.com%252F%26ntime%3D1489231442",
    "CNZZDATA4263708" : r"cnzz_eid%3D1082735085-1489276502-null%26ntime%3D1489286147",
    "Hm_lvt_c1d6d6bb63e3609ec44b40985345956b" : r"1489276505,1489286150",
    "Hm_lpvt_c1d6d6bb63e3609ec44b40985345956b" : r"1489286150",
    "CNZZDATA5597968" : r"cnzz_eid%3D1959441223-1489439576-http%253A%252F%252Fwww.cnblogs.com%252F%26ntime%3D1489439576",
    "CNZZDATA1252954968" : r"1157509149-1489795924-null%7C1489818838",
    "CNZZDATA1257397063" : r"1231317826-1490001962-http%253A%252F%252Fwww.cnblogs.com%252F%7C1490054406",
    "CNZZDATA1000228226" : r"207945390-1490178058-http%253A%252F%252Fwww.cnblogs.com%252F%7C1490178420",
    "CNZZDATA1465781" : r"cnzz_eid%3D1283741302-1490192068-null%26ntime%3D1490192068",
    "CNZZDATA5068810" : r"cnzz_eid%3D179574360-1490171416-null%26ntime%3D1490861868",
    "CNZZDATA1258390419" : r"1749241138-1491137279-http%253A%252F%252Fwww.cnblogs.com%252F%7C1491137279",
    "lhb_smart_1" : r"1",
    "Hm_lvt_cec7b3b7ecb170891406ea59237c9168" : r"1492015045,1492015091,1492015099",
    "Hm_lpvt_cec7b3b7ecb170891406ea59237c9168" : r"1492015099",
    "CNZZDATA5882415" : r"cnzz_eid%3D512596388-1492216854-null%26ntime%3D1492216854",
    "CNZZDATA4810808" : r"cnzz_eid%3D679032637-1492218351-null%26ntime%3D1492218351",
    "CNZZDATA3167937" : r"cnzz_eid%3D894407411-1492522681-http%253A%252F%252Fwww.cnblogs.com%252F%26ntime%3D1492522681",
    "CNZZDATA1261691463" : r"836724154-1492902166-null%7C1492902166",
    "__utmz" : r"226521935.1493461984.5.5.utmcsr",
    "AJSTAT_ok_times" : r"6",
    "CNZZDATA1121896" : r"cnzz_eid%3D322529524-1490063022-null%26ntime%3D1493634274",
    "CNZZDATA943648" : r"cnzz_eid%3D1465561481-1490064025-null%26ntime%3D1493632639",
    "CNZZDATA2236510" : r"cnzz_eid%3D976389971-1493633620-null%26ntime%3D1493633620",
    "CNZZDATA1252921082" : r"2010858328-1494039306-http%253A%252F%252Fwww.cnblogs.com%252F%7C1494039308",
    "CNZZDATA2686777" : r"cnzz_eid%3D93711210-1492495321-null%26ntime%3D1494221137",
    "CNZZDATA4106998" : r"cnzz_eid%3D1901650634-1494417729-null%26ntime%3D1494417729",
    "__utma" : r"226521935.770139923.1488933876.1493461984.1494648245.6",
    "__utmc" : r"226521935",
    "jiathis_rdc" : r"%7B%22http%3A//www.cnblogs.com/xishuai/p/visual-studio-for-mac.html%22%3A%220%7C1494648396982%22%7D",
    "CNZZDATA3685059" : r"cnzz_eid%3D718439378-1494411288-null%26ntime%3D1494656318",
    ".CNBlogsCookie" : r"CFEFCB15C26E2BA3ED844796476FF1EC3861D08623EC1713B8DF0BDFF48B5D1521F33774C6D127BBC5AE3958AFD8146A2B4B032CE223BEE6D54F3776E771A5B3A72F4301590C017A7E6837330D9C7E6AA6E38B5CE0E37CC195D74A979F12F323BC0A2003",
    "CNZZDATA1254128672" : r"1721312493-1493211435-http%253A%252F%252Fwww.cnblogs.com%252F%7C1494748726",
    "sc_is_visitor_unique" : r"rx9614694.1494838551.D85D6D78B4614F89AC885E5C72F3011B.3.3.3.3.3.3.3.3.3-10500913.1492495039.1.1.1.1.1.1.1.1.1-11247317.1491466337.2.2.2.2.2.2.2.1.1",
    "CNZZDATA1252961619" : r"410684456-1494079866-null%7C1494853825",
    "CNZZDATA1255738818" : r"322042092-1494822519-%7C1494855449",
    ".Cnblogs.AspNetCore.Cookies" : r"CfDJ8Mmb5OBERd5FqtiQlKZZIG5RjVY8qfQIy7CwqAynBew05RbvmE925-dZPmxViG9Yz5HF8YMxu7bKLVM0nhqhhNrjpVIz8OWH_Lyl9GqYeCuNQCfRa8yuPKDFRKuoJ-7l4BV1heLdpe8l_cmf8b2xKQyVpc20ia8hIGp3JG9dqkaOZn64E-bKELSxSIn-A9jY0SflvCraVcQsO19kRUS6FQk4dul_UJbORAakBlg5zYZ7JOoJ7VV7PqwD0R_zhMSYoGHIw3o_2THzy2-exdyUm2eaMQCrRnVg8zSAMrnscc466s0Hsc5d1k4jTVGlAqHGlA",
    "_gat" : r"1",
    "_ga" : r"GA1.2.770139923.1488933876",
    "_gid" : r"GA1.2.1511577148.1494904255"
}

CNBLOG_MAIN_POST_PAYLOAD = {
    "CategoryType":"SiteHome",
    "ParentCategoryId":0,
    "CategoryId":808,
    "PageIndex":1,
    "TotalPostCount":4000,
    "ItemListActionName":"PostList"
}

CNBLOG_MAIN_POST_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Referer': 'https://www.cnblogs.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

CNBLOG_USER_FOLLOWER_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Referer': 'https://home.cnblogs.com/u/George1994/followers/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

CNBLOG_USER_URL = 'http://www.cnblogs.com/George1994'

CNBLOG_USER_FOLLOWER_URL = 'https://home.cnblogs.com/u/George1994/followers'

# 博客园博主信息界面
CNBLOG_USER_HOME_URL = 'https://home.cnblogs.com'

# 博客园积分排名前3000名的博主
CNBLOG_POPULAR_URL = 'http://www.cnblogs.com/AllBloggers.aspx'

# 博客园博问界面
CNBLOG_QUESTION_URL = 'https://q.cnblogs.com'

SPLASH_URL = 'http://192.168.99.100:8050'

SPLASH_LOG_400 = True

# HTTP高速缓存
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


# 用作登录
CRAWLERA_LOGIN_USER_KEY = 'hsAxJqXH61/i/NTSPKivb2+tm+fEk0NmhVyzFjan1UUyuxsmJz/QYiRCGgKWkPJB2QPmEmpfHFe' \
                    '+RZBKaje0GXtptShHeT/WkQ9ZeiB2KNLits30JpFE18AZOhT/5OPDEYFAxToV4zCLkkISAM6Qd/BOYX1GDeGrH48LJ3gLfWw='
CRAWLERA__LOGIN_PASS_KEY = 'em3EDpJvnK+vpvDjtdtUVVeJchYrWbdSF7HMv9zHNdXSC0LslWP9qiAhlb5LnLXwUAYYJHW1Q2+bcnz1ubNQa' \
                    '/TwUHYPZKJfUhtxpXLYq7Io/LEZGgZT8ENUrLaGIeSLHokW4nG44eUsiYimtbZlwRyDRKMRGYLGeVnO0lhC/XI='

CRAWLERA_LOGIN_REMEMBER = True

DUPEFILTER_DEBUG = True