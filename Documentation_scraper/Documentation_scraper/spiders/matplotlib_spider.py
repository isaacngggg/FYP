import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose           ## only a few examples of Processors that can manupulate data
from Documentation_scraper.items import PropertiesItem
import socket
import datetime
import urllib.parse as urlparse
from scrapy.http import Request

import re

class MySpider(CrawlSpider):
    name = 'matplotlib_spider'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org']

    rules = (
        #Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,''"admonition seealso")]'), callback ='parse_item', follow = True),
        Rule(LinkExtractor(allow = ('.*matplotlib.org/stable/.*matplotlib..*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*matplotlib.org/stable'),deny = ('.*matplotlib.org/1.*'))),
        #Rule(LinkExtractor(allow = ".*numpy\.org\/doc\/stable.*",), follow = True, callback='parse'),
        )


    def parse(self, response):
        # Parse each quote div 
        item=PropertiesItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('/html/body/div[2]/div/main/div/div[1]/article/section/dl/dd/p[1]/text()').get()
        item['url'] = response.url
        item['spider'] = self.name
        
        yield item