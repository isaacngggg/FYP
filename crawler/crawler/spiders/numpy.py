
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider

from scrapy.loader import ItemLoader
from crawler.items import crawlerItem
from . import normalise


class NumpySpider(CrawlSpider):
    name = "numpy"
    allowed_domains = ["numpy.org"]
    start_urls = ["http://numpy.org/"]
    
    rules = (

        Rule(LinkExtractor(allow = ('.*numpy.org/doc/stable/reference/generated/numpy..*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*numpy.org/doc/'),deny = ('.*numpy.org/doc/1.*'))),
        
        )

    def parse(self, response):
        # Parse each quote div 
        item=crawlerItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('//article/section/dl/dd/p[1]/text()').get()
        item['normalisedDescription'] = normalise(item['description'])
        item['url'] = response.url
        item['spider'] = self.name
        
        yield item
