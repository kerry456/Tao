# -*- coding: utf-8 -*-
import json
import time

import scrapy
from Tao.settings import *
from urllib import parse
from Tao.items import TaoItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    base_url='https://s.taobao.com/search?search_type=item' \
             '&ssid=s5-e&commend=all&imgfile=&q={}' \
             '&_input_charset=utf-8&wq=&suggest_query=&source=suggest' \
             '&sort=sale-desc&bcoffset=0&p4ppushleft=%2C{}&s={}'
    # allowed_domains = ['taobao.com']
    # start_urls = ['http://taobao.com/']
    def start_requests(self):
        key_words = self.settings['KEY_WORDS']
        key_words = parse.quote(key_words,safe=' ').replace(' ','+')
        page_num = self.settings['PAGE_NUM']
        one_page_count = self.settings['ONE_PAGE_NUM']
        for i in range(page_num):
            url = self.base_url.format(key_words,one_page_count,i*one_page_count)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        try:
            g_page_config = response.selector.re('g_page_config = ({.*?});')[0]
            g_page_config_dict = json.loads(g_page_config)
            auctions = g_page_config_dict['mods']['itemlist']['data']['auctions']
            for auction in auctions:
                item=TaoItem()
                item['nid']=auction['nid']
                item['category']=auction['category']
                item['item_name']=auction['raw_title']
                item['shop']=auction['nick']
                item['price']=auction['view_price']
                item['link'] = 'https:' + auction['detail_url']
                item['sales']=auction['view_sales']
                item['address']=auction['item_loc']
                item['city'] = None
                yield item
        except:
            print(response.url)
            time.sleep(1)
            yield scrapy.Request(response.url,callback=self.parse)
    def encode_item_name(self,item_name):
        item_name = parse.quote(item_name, safe=' ').replace(' ', '+')
        return item_name








