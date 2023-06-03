
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider

from scrapy.loader import ItemLoader
from crawler.items import crawlerItem
from . import normalise


class NumpySpider(CrawlSpider):
    name = "scrapy"
    allowed_domains = ["docs.scrapy.org"]
    start_urls = ["https://docs.scrapy.org/en/latest/topics/api.html"]
    
    rules = (

        Rule(LinkExtractor(allow = ('https://docs.scrapy.org/en/latest/topics/api.html.*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*docs.scrapy.org/en/latest/topics/.*'))),
        
        )

    def parse(self, response):
        # Parse each quote div 
        item=crawlerItem()
        methods = response.css('.py-class')
        for method in methods: 
            print (method.css('dt::attr(id)').get())
            print (method.css('p::text').get())
            item['title'] = method.css('dt::attr(id)').get()
            pArray = method.css('p::text').getall()
            item['description'] = normalise(" ".join(pArray),synon=False)
            item['normalisedDescription_stem'] = normalise(item['description'],stem = True, lemma = False, synon=False)
            item['normalisedDescription_lem'] = normalise(item['description'],stem = False, lemma = True, synon=False)
            item['normalisedDescription_stem_lem'] = normalise(item['description'],stem = True, lemma = True, synon=False)
            item['normalisedDescription_synon'] = normalise(item['description'],stem = False, lemma = True, synon=True)
            item['url'] = response.url
            item['spider'] = self.name
            yield item

        """
            response.css('p::text').getall()
        """