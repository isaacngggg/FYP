from pymongo import MongoClient
import numpy as np
import requests
from bson.objectid import ObjectId

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

tokenized_corpus, corpus, IDs = fetchAllMongo()

while (1):
    user_input = input ("Enter Description: ")
    scoreBERT = np.array(queryBERT(user_input,corpus))
    # print (scoreBERT)
    # print (corpus[np.argmax(scoreBERT)])
    #print (des[np.argmax(data)])
    sortedBertArr = np.argsort(-scoreBERT)
    # print (sortedBertArr)
    printtop_n (sortedBertArr,IDs)