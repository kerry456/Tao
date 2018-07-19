# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql
from Tao.items import TaoItem

class TaoPipeline(object):
    def process_item(self, item, spider):
        item['sales'] = int(item['sales'].replace('人收货', ''))
        item['price'] = float(item['price'])
        # address = item.pop('address').split(' ')
        # # item['province'] = address[0]
        # if len(address) > 1:
        #     item['city'] = address[0]
        # else:
        #     item['city'] = ''
        return item
class TaoscrapyPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'taobao')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db['taobao'].insert_one(dict(item))
        print('插入mongo数据库成功')
        return item
class TaoMysqlPipeline(object):
    def open_spider(self,spider):
        try:
            self.conn = pymysql.connect(host='182.92.225.115', port=13306, user='root', passwd='spider', db='taobao',use_unicode = True,charset='utf8')
            self.cursor = self.conn.cursor()
            print('连接成功。。。')
        except Exception as e:
            print('数据库连接失败。。',e)
    def process_item(self, item, spider):
        if isinstance(item,TaoItem):
            try:
                insert_sql = ''' INSERT INTO taobao(NID,CATEGORY,NAME,SHOP,PRICE,LINK,SALES,CITY)  VALUES ("{}","{}","{}","{}","{}","{}","{}","{}")'''.format(item['nid'],item['category'],item['item_name'],item['shop'],item['price'],item['link'],item['sales'],item['address'])
                self.cursor.execute(insert_sql)
                self.conn.commit()
                print('数据插入成功。。')
            except Exception as e:
                print('数据插入失败。。',e)
        return item
    def close_spider(self):
        self.conn.close()
















