import pymongo
from bson.regex import Regex
from bson.objectid import ObjectId

from crawler.settings import MONGODB_DB, MONGODB_URI

class MongoIndexer(object):
    
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        
    def connect(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
        
    def close(self):
        self.client.close()
        
    def index(self, item):
        self.collection.insert_one(dict(item))
        
    def search(self, query):
        regex = Regex('.*{}.*'.format(query), 'i')
        results = self.collection.find({'$or': [
            {'title': {'$regex': regex}},
            {'description': {'$regex': regex}}
        ]})
        return list(results)
    
    def get(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})

indexer = MongoIndexer(MONGODB_URI, MONGODB_DB, 'all')
indexer.connect()

# Search for documents
query = input ('Search for any function: ')
results = indexer.search(query)
print(results)

# Close the connection
indexer.close()

