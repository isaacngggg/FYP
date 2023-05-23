from pymongo import MongoClient
import numpy as np
import requests
import time
from bson.objectid import ObjectId

from rank_bm25 import BM25Okapi

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {'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'}"}

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
    corpus = np.array(corpus)
    IDs = np.array(IDs)
    return tokenized_corpus, corpus, IDs

def queryBERT(user_input,corpus):
    response = requests.post(API_URL, headers=headers, 
                             json={ "inputs": {
                                            "source_sentence": user_input,
                                            "sentences": corpus }})
    return response.json()

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

def normalise (description):
    tokens = word_tokenize(description)
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in tokens]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in stemmed_words if word.lower() not in stop_words]
    normalisedDescription = filtered_words
    return normalisedDescription

def getArr_BM25Top_n (tokenized_corpus,normalised_query,n = 50):
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.array(bm25.get_scores(normalised_query))
    sorted = np.argsort(-doc_scores)
    return sorted[:n]

def timestampSinceLast(note = 'timestamp'):
    now = time.time()
    rounded_value = np.around(now-last, decimals=3)
    print('\n'+ note + ': '+ str(rounded_value) + ' seconds'+'\n')

last = time.time()
tokenized_corpus, corpus, IDs = fetchAllMongo()
last = timestampSinceLast('Fetched')

while (1):
    n = 300
    user_input = input ("Enter Description: ")
    normalised_query = normalise(user_input)
    last = time.time()
    topN_BM25Arr = getArr_BM25Top_n(tokenized_corpus,normalised_query, n)
    last = timestampSinceLast('BM25')
    topN_corpus = corpus[topN_BM25Arr].tolist()
    #print (topN_corpus)
    topN_IDs = IDs[topN_BM25Arr].tolist()
    print(topN_IDs)
    last = time.time()
    scoreBERT = np.array(queryBERT(user_input,topN_corpus))
    last = timestampSinceLast('queryBERT (' + str(n) +' times)')
    sortedBertArr = np.argsort(-scoreBERT)
    #print (np.shape(scoreBERT))
    printtop_n (sortedBertArr,topN_IDs)