from pymongo import MongoClient
import numpy as np

from bson.objectid import ObjectId


from rank_bm25 import BM25Okapi
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
        print ('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

def printDoc (document):
    print ('Title: ' + document ['title'])
    print ('Description: ' +document ['description']+'\n')
    
def fetchAllMongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['all']
    projection = {'normalisedDescription': 1, 'description': 1, '_id':1,'title':1}
    cursor = collection.find({}, projection)

    tokenized_corpus = []
    corpus = []
    IDs = []
    titles = []
    for document in cursor:
        tokenized_corpus += [document['normalisedDescription']]
        corpus += [document['description']]
        IDs += [document['_id']]
        titles += [document['title']]
    client.close()
    
    return tokenized_corpus, corpus, IDs, titles


def getIDs_BM25Top_n (tokenized_corpus,normalised_query,n = 50):
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.array(bm25.get_scores(normalised_query))
    return np.argsort(-doc_scores)
def main():
    tokenized_corpus, corpus, IDs, titles = fetchAllMongo()

    query = "maximum arg"
    normalised_query = normalise(query)

    sortedBM25Arr = getIDs_BM25Top_n(normalised_query)
    printtop_n(sortedBM25Arr,IDs)


