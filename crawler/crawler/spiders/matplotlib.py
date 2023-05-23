
from scrapy.linkextractors import LinkExtractor
from crawler.items import crawlerItem

from scrapy.spiders import CrawlSpider, Rule
from . import normalise

class MatplotlibSpider(CrawlSpider):
    name = "matplotlib"
    allowed_domains = ["matplotlib.org"]
    start_urls = ["http://matplotlib.org/"]

    rules = (
        #Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,''"admonition seealso")]'), callback ='parse_item', follow = True),
        Rule(LinkExtractor(allow = ('.*matplotlib.org/stable/.*matplotlib..*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*matplotlib.org/stable'),deny = ('.*matplotlib.org/1.*'))),
        #Rule(LinkExtractor(allow = ".*numpy\.org\/doc\/stable.*",), follow = True, callback='parse'),
        )


    def parse(self, response):
        # Parse each quote div 
        item=crawlerItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('/html/body/div[2]/div/main/div/div[1]/article/section/dl/dd/p[1]/text()').get()
        item['normalisedDescription'] = normalise(item['description'])
        item['url'] = response.url
        item['spider'] = self.name
        
        yield item
