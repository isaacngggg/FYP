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
    name = 'numpy_spider'
    allowed_domains = ['numpy.org']
    start_urls = ['https://numpy.org']

    rules = (

        Rule(LinkExtractor(allow = ('.*numpy.org/doc/stable/reference/generated/numpy..*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*numpy.org/doc/'),deny = ('.*numpy.org/doc/1.*'))),
        
        )

    
    def parse(self, response):
        # Parse each quote div 
        item=PropertiesItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('//article/section/dl/dd/p[1]/text()').get()
        item['url'] = response.url
        item['spider'] = self.name
        
        yield item

