# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class MiddleproPipeline:
    def process_item(self, item, spider):
        filename ='d:\\novel\\xinwen\\' + item['title'] + '.txt'
        try:
            # 有一些特殊符号:\/*?<>之类的不能作为文件名
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(item['title'])
                f.write(item['content'])
        except Exception as e:
            m = spider.n
            with open(f'd:\\novel\\xinwen\\{m}.txt', 'w', encoding='utf-8') as f:
                print('ok')
                f.write(item['title'])
                f.write(item['content'])
            spider.n += 1
