
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
# Retrieve the form data from command-line arguments
query = sys.argv[1]


testIDs = [ObjectId('643e5cfe66e0318c8e461fa8'), ObjectId('643e5d1c66e0318c8e462177'), ObjectId('643e5d1e66e0318c8e4621af'),ObjectId('643e5d2566e0318c8e46226a')]

def fetchMongobyID (ID):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['all']
    projection = {'_id': 0}
    document = collection.find_one({"_id": ID},projection)
    #print (document)
    client.close()
    return document

def printResults (testIDs):
    for id in testIDs:
        print(fetchMongobyID(id))

fetchedArr = []
for id in testIDs:
    fetchedArr += [fetchMongobyID(id)]
json_data = json.dumps(fetchedArr)
print(json_data)
