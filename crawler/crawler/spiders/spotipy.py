
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider

from scrapy.loader import ItemLoader
from crawler.items import crawlerItem
from . import normalise


class NumpySpider(CrawlSpider):
    name = "spotipy"
    allowed_domains = ["spotipy.readthedocs.io"]
    start_urls = ["https://spotipy.readthedocs.io/en/2.22.1/"]
    
    rules = (

        Rule(LinkExtractor(allow = ('.*spotipy.readthedocs.io/en/2.22.1.*')), callback ='parse'),
        Rule(LinkExtractor(allow = ('.*spotipy.readthedocs.io/en/.*'))),
        
        )

    def parse(self, response):
        # Parse each quote div 
        item=crawlerItem()
        methods = response.css('.method')
        for method in methods: 
            print (method.css('dt::attr(id)').get())
            print (method.css('p::text').get())
            item['title'] = method.css('dt::attr(id)').get()
            item['description'] = method.css('p::text').get()
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
