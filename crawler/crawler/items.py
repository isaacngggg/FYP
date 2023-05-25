# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class crawlerItem(scrapy.Item):
    
    title = scrapy.Field()
    description = scrapy.Field()
    normalisedDescription = scrapy.Field()
    
    url = scrapy.Field()
    spider = scrapy.Field()


class pypiItem(scrapy.Item):
    
    title = scrapy.Field()
    description = scrapy.Field()
    normalisedDescription = scrapy.Field()
    installMethod = scrapy.Field()
    
    gitHub = scrapy.Field()
    gitHubStar = scrapy.Field()
    
    
    url = scrapy.Field()
    spider = scrapy.Field()