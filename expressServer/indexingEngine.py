
import sys
import json
# Retrieve the form data from command-line arguments
query = sys.argv[1]
n = int(sys.argv[2])
# query = "maximum array"
# n = 20
# if (n < 1):
#     n = 5

from pymongo import MongoClient
import numpy as np
import requests
import time
from bson.objectid import ObjectId

from rank_bm25 import BM25Okapi

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {'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'}"}

import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def normalise (text,lemma = True,stem = False,synon = True):
    normalisedDescription = []
    tokens = word_tokenize(text)
    tokens_without_punctuation = [token for token in tokens if not any(char in string.punctuation for char in token)]
    stop_words = set(stopwords.words('english'))
    normalisedDescription = [word for word in tokens_without_punctuation if word.lower() not in stop_words]
    if lemma:
        lemmatizer = WordNetLemmatizer()
        normalisedDescription = [lemmatizer.lemmatize(token) for token in normalisedDescription]
    if stem:
        stemmer = PorterStemmer()
        normalisedDescription = [stemmer.stem(word) for word in normalisedDescription]
    if synon:
        normalisedDescription = replace_synonyms(normalisedDescription)
    return normalisedDescription

def replace_synonyms(tokens):
    replaced_tokens = []
    for token in tokens:
        synsets = wordnet.synsets(token)
        if synsets:
            first_synset = synsets[0]
            lemma_names = first_synset.lemma_names()
            if lemma_names:
                replaced_token = lemma_names[0]
                replaced_tokens.append(replaced_token)
            else:
                replaced_tokens.append(token)
        else:
            replaced_tokens.append(token)
    return replaced_tokens

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

def getTopN_IDs (sortedBertArr, IDs,n):
    TopN_ids = []
    for i in range (0,n):
        TopN_ids += [IDs[sortedBertArr[i]]]
    return TopN_ids

def getArr_BM25Top_n (tokenized_corpus,normalised_query,n):
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.array(bm25.get_scores(normalised_query))
    sorted = np.argsort(-doc_scores)
    return sorted[:n]

def timestampStart():
    return time.time()

def timestampSince(last):
    now = time.time()
    rounded_value = np.around(now-last, decimals=3)
    return rounded_value

def fetchMongobyID (ID):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['all']
    projection = {'_id': 0}
    document = collection.find_one({"_id": ID},projection)
    client.close()
    return document

def addTimeMongo (overallTime,mongoTime,BM25Time,bertTime,n,query):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['timeStamps']
    new_document = {
        'Overall timelapse': overallTime,
        'Time to fetchMongo': mongoTime,
        'Time to BM25': BM25Time,
        'Time for Bert to index': bertTime,
        'N value': n,
        'query': query
    }
    collection.insert_one(new_document)
    client.close()

start = timestampStart()
tokenized_corpus, corpus, IDs = fetchAllMongo()
mongoTime = timestampSince(start)
normalised_query = normalise(query)
bm25start = timestampStart()
topN_BM25Arr = getArr_BM25Top_n(tokenized_corpus,normalised_query, n)

topN_corpus = corpus[topN_BM25Arr].tolist()
topN_IDs = IDs[topN_BM25Arr].tolist()
BM25Time = timestampSince(bm25start)
bertstart = timestampStart()
scoreBERT = np.array(queryBERT(query,topN_corpus))
bertTime = timestampSince(bertstart)

sortedBertArr = np.argsort(-scoreBERT)
TopN_ids = getTopN_IDs(sortedBertArr,topN_IDs,n = 10)
fetchedArr = []
for id in TopN_ids:
    fetchedArr += [fetchMongobyID(id)]
json_data = json.dumps(fetchedArr)
overallTime = timestampSince(start)
addTimeMongo (overallTime,mongoTime,BM25Time,bertTime,n,query)
print(json_data)