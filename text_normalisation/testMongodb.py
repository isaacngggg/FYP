from pymongo import MongoClient

# Connect to the local MongoDB instance
client = MongoClient('mongodb://localhost:27017/')

# Access a specific database
db = client['scrapped-function']

# Access a specific collection within the database
collection = db['all']



# Close the connection to MongoDB
client.close()
