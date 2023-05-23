# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
from itemadapter import ItemAdapter
from scrapy import settings

import queryApp as queryApp
import sys
from .items import PropertiesItem
from .settings import MONGODB_URI, MONGODB_DB

class MongoDBPipeline ():
    # def __init__(self, mongodb_uri, mongodb_db):
    #     self.mongodb_uri = mongodb_uri
    #     self.mongodb_db = mongodb_db
    #     if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")
    def __init__(self):
        self.mongodb_uri = MONGODB_URI
        self.mongodb_db = MONGODB_DB
        
    #@classmethod
    #  def from_crawler(cls, crawler):
    #     return cls(
    #         mongodb_uri=crawler.settings.get('MONGODB_URI'),
    #         mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'PropertiesItem')
    #     )

    def open_spider(self, spider):
        collection = spider.name
        self.client = queryApp.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = spider.name
        data = dict(PropertiesItem(item))
        self.db[collection].insert_one(data)
        return item



class DocumentationScraperPipeline:
    def process_item(self, item, spider):
        
        return item

class VerifyFunctionPipeline:
    def __init__(self):
        self.ids_seen = set()
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if re.match (r".*\..*",adapter['title']):
            return item
        else:
            raise DropItem(f"Not a function: {item!r}")
            
    
class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item
        
        
