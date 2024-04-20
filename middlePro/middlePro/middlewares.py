# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import fake_useragent
from fake_useragent import UserAgent
import random
from scrapy.http import HtmlResponse
from time import sleep

class MiddleproSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MiddleproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # 代理ip列表
    PROXY_http = [
        '153.180.102.104: 80',
    ]
    PROXY_https = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    # 拦截请求
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        '''UA伪装。为了确保每一个请求的UA不一样，可以封装UA池，UA池其实就是列表'''
        ua = UserAgent()
        request.headers['User-Agent'] = ua.chrome



        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    # 拦截响应。进行篡改，使其满足要求
    def process_response(self, request, response, spider):  # spider表示爬虫对象
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        # 获取了爬虫类中定义地浏览器对象
        bro = spider.bro
        # 挑选出指定的响应对象进行篡改。通过url指定request, 通过request指定response对象
        if request.url in spider.model_urls:
            bro.get(request.url)    # 五个板块对应的url进行请求。打开网址
            sleep(3)
            # 包含了动态加载的新闻数据
            page_text = bro.page_source
            # 五大板块对应的请求对象
            # 针对对应到的response进行篡改
            # 实例化一个新的符合1需求的响应对象（包含动态加载出的新闻数据）替代原来旧的response
            # HtmlResponse(url, body, encoding, request)
            # 如何获取动态加载出的新闻数据？可以使用selenium
                # 基于selenium可以很便捷地获取动态加载数据
            new_response = HtmlResponse(request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        else:
            return response

        # return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

        '''代理ip，当请求发生异常时，该方法拦截到异常请求，对其进行修订'''
        if request.url.split(':')[0] == 'http':
            request.meta['proxy'] = 'http' + random.choice(self.PROXY_http)
        else:
            request.meta['proxy'] = 'https' + random.choice(self.PROXY_https)
        return request  # 将修正之后的请求对象进行重新发送

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
