
import numpy as np
import time
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


def normalise (text,lemma = False,stem = False,synon = False, printSynon = False):
    normalisedDescription = []
    tokens = word_tokenize(text)
    tokens_without_punctuation = [token.lower() for token in tokens if not any(char in string.punctuation for char in token)]
    stop_words = set(stopwords.words('english'))
    normalisedDescription = [word for word in tokens_without_punctuation if word.lower() not in stop_words]
    if lemma:
        lemmatizer = WordNetLemmatizer()
        normalisedDescription = [lemmatizer.lemmatize(token) for token in normalisedDescription]
    if stem:
        stemmer = PorterStemmer()
        normalisedDescription = [stemmer.stem(word) for word in normalisedDescription]
    if synon:
        lemmatizer = WordNetLemmatizer()
        normalisedDescription = [lemmatizer.lemmatize(token) for token in normalisedDescription]
        if printSynon:    
            normalisedDescription = replace_synonyms(normalisedDescription,printSyn=True)
        else: 
            normalisedDescription = replace_synonyms(normalisedDescription)
    return normalisedDescription

def replace_synonyms(tokens,printSyn = False):
    replaced_tokens = []
    for token in tokens:
        synsets = wordnet.synsets(token)
        if synsets:
            first_synset = synsets[0]
            lemma_names = first_synset.lemma_names()
            if lemma_names:
                if printSyn:
                    print (f"Synonom Group for {token}: {lemma_names}")
                replaced_token = lemma_names[0]
                replaced_tokens.append(replaced_token)
            else:
                replaced_tokens.append(token)
        else:
            replaced_tokens.append(token)
    return replaced_tokens

from pymongo import MongoClient
    
def fetchAllMongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['scrapped-function']
    collection = db['all']
    projection = {'spider': 0, 'url': 0}
    cursor = collection.find({}, projection)

    stemDes = []
    lemDes = []
    stemLemDes = []
    synonDes = []
    des = []
    ids = []
    titles = []
    for document in cursor:
        des += [document['description']]
        ids += [document['_id']]
        titles += [document['title']]
        stemDes += [document['normalisedDescription_stem']]
        lemDes += [document['normalisedDescription_lem']]
        stemLemDes += [document['normalisedDescription_stem_lem']]
        synonDes += [document['normalisedDescription_synon']]
    client.close()

    return ids,titles,des,stemDes,lemDes,stemLemDes,synonDes

from rank_bm25 import BM25Okapi


def getRanksArr (queries,funcs,normalMethod,b = 0.75,k1 = 1.5):
    ids,titles,des,stemDes,lemDes,stemLemDes,synonDes = fetchAllMongo()
    RanksArr = []
    rankings = []
    actualDescriptions = []
    fetchedTitles = []
    if normalMethod == 'stem' :
        bm25 = BM25Okapi(stemDes,b=b,k1=k1)
        #print ("Norm method: stem")
    elif normalMethod == 'lem' :
        bm25 = BM25Okapi(lemDes,b=b,k1=k1)
        #print ("Norm method: lem")
    elif normalMethod == 'synon' :
        bm25 = BM25Okapi(synonDes,b=b,k1=k1)
        #print ("Norm method: Synon")
    else :
        print ("ERROR: no valid method")
        exit()
    for j in range (0, len(queries)):
        query = queries[j]
        # normalisedDes = [normalise(text,stem = False,lemma = True, synon=True) for text in des]
        normalised_query = normaliseByMethod (query,normalMethod)
        scores = np.array(bm25.get_scores(normalised_query))  
        sortedIndices = np.argsort(-scores)
        sortedTitles = [titles[i] for i in sortedIndices]
        RanksArr += [i for i, value in enumerate(sortedTitles) if value == funcs[j]]
        
    return RanksArr

def getBM25Arrays (query,func,normalMethod,n,b = 0.75,k1 = 1.5):
    ids,titles,des,stemDes,lemDes,stemLemDes,synonDes = fetchAllMongo()
    if normalMethod == 'stem' :
        corpus = stemDes
    elif normalMethod == 'lem' :
        corpus = lemDes
        #print ("Norm method: lem")
    elif normalMethod == 'stemLem' :    
        corpus = stemLemDes
        #print ("Norm method: stemLem")
    elif normalMethod == 'synon' :
        corpus = synonDes
    else :
        print ("ERROR: no valid method")
        exit()
    bm25 = BM25Okapi(corpus,b=b,k1=k1)
    # normalisedDes = [normalise(text,stem = False,lemma = True, synon=True) for text in des]
    normalised_query = normaliseByMethod (query,normalMethod)
    scores = np.array(bm25.get_scores(normalised_query))  
    sortedIndices = np.argsort(-scores)
    sortedTitles = [titles[i] for i in sortedIndices]
    sortedDes = [des[i] for i in sortedIndices]
    BM25Rank = [i for i, value in enumerate(sortedTitles) if value == func]

    slicedTitles = sortedTitles[:n]
    slicedDescription = sortedDes[:n]
    
    return slicedTitles,slicedDescription, BM25Rank

def normaliseByMethod (query,normalMethod):
    if normalMethod == 'stem' :
        normalised_query = normalise(query,stem = True)
    elif normalMethod == 'lem' :
        normalised_query = normalise(query,lemma = True)
    elif normalMethod == 'synon' :
        normalised_query = normalise(query,synon=True)
    else :
        print ("ERROR: no valid method")
        exit()
    return normalised_query

def timeStart():
    return time.time()

def timeSince(last):
    now = time.time()
    rounded_value = np.around(now-last, decimals=3)
    return rounded_value

import requests
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {'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'}"}

def queryBERT(user_input,corpus):
    while True:
        try:
            bertStart = timeStart()
            response = requests.post(API_URL, headers=headers, 
                                    json={ "inputs": {
                                                    "source_sentence": user_input,
                                                    "sentences": corpus }},timeout= 5)
            
            if response.status_code == 200:
                bertTime = timeSince(bertStart)
                return response.json(),bertTime
        except requests.exceptions.Timeout:
            print("Timeout error occurred. Retrying...")
        except requests.exceptions.ReadTimeout:
            print("ReadTimeout error occurred. Retrying...")
        except requests.exceptions.RequestException as e:  
            print(f"An error occurred: {e}")  
        time.sleep(3)
