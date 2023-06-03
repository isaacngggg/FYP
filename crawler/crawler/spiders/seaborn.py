
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider

from scrapy.loader import ItemLoader
from crawler.items import crawlerItem
from . import normalise


class NumpySpider(CrawlSpider):
    name = "seaborn"
    allowed_domains = ["seaborn.pydata.org"]
    start_urls = ["https://seaborn.pydata.org/generated/seaborn.objects.Plot.html"]
    
    rules = (

        Rule(LinkExtractor(allow = ('.*seaborn.pydata.org/generated/seaborn..*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*seaborn.pydata.org/generated.*'))),
        
        )

    def parse(self, response):
        # Parse each quote div 
        item=crawlerItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('//article/section/dl/dd/p[1]/text()').get()
        item['normalisedDescription_stem'] = normalise(item['description'],stem = True, lemma = False, synon=False)
        item['normalisedDescription_lem'] = normalise(item['description'],stem = False, lemma = True, synon=False)
        item['normalisedDescription_stem_lem'] = normalise(item['description'],stem = True, lemma = True, synon=False)
        item['normalisedDescription_synon'] = normalise(item['description'],stem = False, lemma = True, synon=True)
        pArray = response.css('p:not([class])::text').getall()
        item['normalisedBody'] = normalise(" ".join(pArray),synon=False)
        item['url'] = response.url
        item['spider'] = self.name
        
        yield item

        """
            response.css('p::text').getall()
        """