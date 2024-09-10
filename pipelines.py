# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os

class TaobaoPipeline:
    def process_item(self, item, spider):
        return item

class Pipeline_toCSV(object):
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/spiders/Taobao.csv'
        self.file = open(store_file, 'w', encoding='utf-8')
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        if item['image']:
            self.writer.writerow((item['image'],\
                                  item['price'],\
                                  item['deal'],\
                                  item['title'],\
                                  item['shop'],\
                                  item['location']))
        return item

    def close_spider(self, spider):
        self.file.close()
