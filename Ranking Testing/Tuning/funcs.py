
import numpy as np
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def normalise (text,lemma = True,stem = False,synon = True):
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


def getScores (tokenized_corpus,normalised_query):
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.array(bm25.get_scores(normalised_query))
    return np.sort(-doc_scores)

def getRanksArr (queries,funcs):
    ids,titles,des,stemDes,lemDes,stemLemDes,synonDes = fetchAllMongo()
    RanksArr = []
    rankings = []
    actualDescriptions = []
    fetchedTitles = []
    for j in range (0, len(queries)):
        query = queries[j]
        normalised_query = normalise(query,stem = False,lemma = True, synon=True)
        normalisedDes = [normalise(text,stem = False,lemma = True, synon=True) for text in des]
        bm25 = BM25Okapi(normalisedDes)
        scores = np.array(bm25.get_scores(normalised_query))  
        sortedIndices = np.argsort(-scores)
        sortedTitles = [titles[i] for i in sortedIndices]
        RanksArr += [i for i, value in enumerate(sortedTitles) if value == funcs[j]]
        
    return RanksArr

import pandas as pd

df = pd.read_csv('data.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])


print (getRanksArr (queries,funcs))

