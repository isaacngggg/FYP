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
    name = 'spotipy_spider'
    allowed_domains = ['spotipy.readthedocs.io']
    start_urls = ['https://spotipy.readthedocs.io/en/2.22.1/']

    rules = (
        #Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,''"admonition seealso")]'), callback ='parse_item', follow = True),
        Rule(LinkExtractor(allow = ('.*spotipy.readthedocs.io/en/2.22.1/.*')), callback ='parse_item'),
        Rule(LinkExtractor(allow = ('.*spotipy.readthedocs.io'),)),
        #Rule(LinkExtractor(allow = ".*numpy\.org\/doc\/stable.*",), follow = True, callback='parse'),
        )
    def parse_item(self, response):                                  ## Same thing as the python shell response
        
        l = ItemLoader(item=PropertiesItem(), response=response)
        
        response.css('method').getall()
        
        l.add_css('title','descname')
        l.add_css('description','//article/section/dl/dd/p[1]/text()')
        
        l.add_value('url', response.url)                                        
        l.add_value('spider', self.name)
        return l.load_item()
    
    
