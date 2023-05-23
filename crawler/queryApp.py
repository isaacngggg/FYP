import pymongo

MONGODB_DB = "scrapped-function"
MONGODB_URI = "mongodb://localhost:27017"
# Connect to the MongoDB instance
client = pymongo.MongoClient(MONGODB_URI)

# Select the database and collection you want to use
db = client[MONGODB_DB]
collection = db['all']

while (1):
    site = input ("Type in your site of choice: \n")
    # Find a document in the collection
    function = input ("Function name: ")
    document = collection.find({"description": { "$regex": '/.*function.*/'}})
    print(document)

# Print the document
