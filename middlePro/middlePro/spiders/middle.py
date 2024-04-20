import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from middlePro.items import MiddleproItem
class MiddleSpider(scrapy.Spider):
    name = "middle"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://news.163.com/"]

    model_urls = []
    n = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    s = Service(executable_path=r'D:\python\Lib\site-packages\chromedriver.exe')

    # 实例化一个浏览器对象
    # def __int__(self):
    bro = webdriver.Chrome(options=options, service=s)


    # 解析五大板块对应的详情页的url
    def parse(self, response):
        url_list = response.xpath('//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [1, 2,  4] # 存储5个板块对应的详情页
        for i in  alist:
            model_url = url_list[i].xpath('./a/@href').extract_first()
            self.model_urls.append(model_url)
        # 依次对每个板块对应的页面进行请求
        for url in self.model_urls:
            yield scrapy.Request(url, callback=self.parse_model)

    # 用来解析每一个板块页面中对应新闻的标题和新闻详情页的url
    def parse_model(self, response):
        div_list = response.xpath('/html/body/div/div[3]/div[3]/div[1]/div[1]/div/ul/li/div/div')
        for div in div_list:
            item = MiddleproItem()
            title = div.xpath('./div/div/h3/a/text() | ./div/h3/a/text()').extract_first()
            if title:
                item['title'] = title.replace(' ', '').replace('\n', '').replace(':', '：')
                new_detail_url = div.xpath('./div/div/h3/a/@href | ./div/h3/a/@href').extract_first()

                # 对新闻详情页的url进行请求
                yield scrapy.Request(new_detail_url, callback=self.parse_detali, meta={'item': item, 'url': new_detail_url})

    def parse_detali(self, response):
        item = response.meta.get('item')
        second_url = response.meta.get('url')
        # new_url_second = response.meta.get('url')
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        if content:
            content = ''.join(content)
            item['content'] = content
            yield item
        else:
            self.model_urls.append(second_url)
            yield scrapy.Request(second_url, callback=self.parse_detail_second, meta={'item': item, 'url': second_url})



    def parse_detail_second(self, response):
        item = response.meta.get('item')
        thrid_url = response.meta.get('url')
        content = response.xpath('//*[@id="content"]/div[2]//text()').extarct()
        content = ''.join(content)
        if not content:
            print(thrid_url)
        item['content'] = content
        yield item

    def closed(self, spider):
        self.bro.close()

