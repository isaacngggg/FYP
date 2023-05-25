# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import pymongo
import re
from .items import crawlerItem, pypiItem
from .settings import MONGODB_URI, MONGODB_DB, DROP_NULL_VALUES_FIELDS,REGEX_VALIDATION_FIELDS

class CrawlerPipeline:
    def process_item(self, item, spider):
        return item

class DropNullValuesPipeline(object):
    
    def __init__(self):
        self.fields_to_check = DROP_NULL_VALUES_FIELDS

    def process_item(self, item, spider):
        for field in self.fields_to_check:
            if not item.get(field):
                raise DropItem(f"Item dropped because {field} is null: {item}")
        return item

class RegexValidationPipeline(object):
    
    def __init__(self):
        self.regex_dict = REGEX_VALIDATION_FIELDS


    def process_item(self, item, spider):
        if isinstance(item, pypiItem):
            print ("regex validation: ignore pypiItem")
            return item
        if isinstance(item,crawlerItem):
            for field, regex in self.regex_dict.items():
                if field not in item:
                    raise DropItem(f"Item dropped because field {field} is missing: {item}")
                value = item[field]
                regex = spider.name + regex
                if not re.match(regex, value):
                    raise DropItem(f"Item dropped because {field} does not match regex '{regex}': {item}")
            return item

class MongoDBPipeline (object):
    # def __init__(self, mongodb_uri, mongodb_db):
    #     self.mongodb_uri = mongodb_uri
    #     self.mongodb_db = mongodb_db
    #     if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")
    def __init__(self):
        self.mongodb_uri = MONGODB_URI
        self.mongodb_db = MONGODB_DB
        self.globalCollectionName = 'placeholder'
        
    #@classmethod
    #  def from_crawler(cls, crawler):
    #     return cls(
    #         mongodb_uri=crawler.settings.get('MONGODB_URI'),
    #         mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'PropertiesItem')
    #     )

    def open_spider(self, spider):
        
        spiderCollection = spider.name
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[spiderCollection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,pypiItem):
            self.globalCollectionName = 'libraries'
            self.globalCollection = self.db[self.globalCollectionName]
        if isinstance(item,crawlerItem):
            self.globalCollectionName = 'all'
            self.globalCollection = self.db[self.globalCollectionName]
        query = {'title': item['title']}
        update = {'$set': dict(item)}
        result = self.globalCollection.update_one(query, update, upsert=True)
        if result.matched_count > 0:
            spider.logger.info(f"Updated item in main MongoDB: {item}")
        else:
            spider.logger.info(f"Inserted new item into main MongoDB: {item}")
        
        spiderCollection = spider.name
        if isinstance(item, pypiItem):
            data = dict(pypiItem(item))
        if isinstance(item, crawlerItem):
            data = dict(crawlerItem(item))
        self.db[spiderCollection].insert_one(data)
        return item

