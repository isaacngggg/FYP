from pymongo import MongoClient
import numpy as np

from bson.objectid import ObjectId
client = MongoClient('mongodb://localhost:27017/')
db = client['scrapped-function']
collection = db['all']
projection = {'normalisedDescription': 1, 'description': 1}
cursor = collection.find({}, projection)


tokenized_corpus = []
corpus = []
for document in cursor:
    tokenized_corpus += [document['normalisedDescription']]
    corpus += [document['description']]
client.close()


from rank_bm25 import BM25Okapi

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def normalise (description):
    tokens = word_tokenize(description)
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in tokens]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in stemmed_words if word.lower() not in stop_words]
    normalisedDescription = filtered_words
    return normalisedDescription



def fetchMongobyID (ID):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['all']
    document = collection.find_one({"_id": ObjectId(ID)})
    #print (document)
    client.close()
    return document

def printtop_n (sortedBertArr, IDs,n = 5):
    for i in range (0,n):
        document = fetchMongobyID (IDs[sortedBertArr[i]])
        printDoc(document)

def printDoc (document):
    print ('Title: ' + document ['title'])
    print ('Description: ' +document ['description']+'\n')
    
def fetchAllMongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['all']
    projection = {'normalisedDescription': 1, 'description': 1, '_id':1}
    cursor = collection.find({}, projection)

    tokenized_corpus = []
    corpus = []
    IDs = []
    for document in cursor:
        tokenized_corpus += [document['normalisedDescription']]
        corpus += [document['description']]
        IDs += [document['_id']]
    client.close()
    
    return tokenized_corpus, corpus, IDs

tokenized_corpus, corpus, IDs = fetchAllMongo()

query = "maximum arg"
normalised_query = normalise(query)

def getIDs_BM25Top_n (normalised_query,n = 50):
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.array(bm25.get_scores(normalised_query))
    return np.argsort(-doc_scores)

sortedBM25Arr = getIDs_BM25Top_n(normalised_query)
printtop_n(sortedBM25Arr,IDs)


