import string
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def normalise (text,lemma = False,stem = False,synon = False):
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
        normalisedDescription = replace_synonyms(normalisedDescription)
    
    return normalisedDescription

def normalise_wLibraryCheck (text,lemma = False,stem = False,synon = False):
    normalisedDescription = []
    tokens = word_tokenize(text)
    tokens_without_punctuation = [token.lower() for token in tokens if not any(char in string.punctuation for char in token)]
    stop_words = set(stopwords.words('english'))
    normalisedDescription = [word for word in tokens_without_punctuation if word.lower() not in stop_words]
    collection, normalisedDescription = libraryCheck(normalisedDescription)
    if lemma:
        lemmatizer = WordNetLemmatizer()
        normalisedDescription = [lemmatizer.lemmatize(token) for token in normalisedDescription]
    if stem:
        stemmer = PorterStemmer()
        normalisedDescription = [stemmer.stem(word) for word in normalisedDescription]
    if synon:
        lemmatizer = WordNetLemmatizer()
        normalisedDescription = [lemmatizer.lemmatize(token) for token in normalisedDescription]
        normalisedDescription = replace_synonyms(normalisedDescription)
    return normalisedDescription,collection

def replace_synonyms(tokens):
    replaced_tokens = []
    for token in tokens:
        synsets = wordnet.synsets(token)
        if synsets:
            first_synset = synsets[0]
            lemma_names = first_synset.lemma_names()
            if lemma_names:
                print (lemma_names)
                replaced_token = lemma_names[0]
                replaced_tokens.append(replaced_token)
            else:
                replaced_tokens.append(token)
        else:
            replaced_tokens.append(token)
    return replaced_tokens



def libraryCheck(normalisedDescription) :
    df = pd.read_csv('libraries.csv')
    libraries = df["libraries"]
    acceptedNames = df["acceptedNames"]
    collection = "all"
    for i in range(len(libraries)):
        names = acceptedNames[i].split(",")
        print (names)
        for name in names:
            if name in normalisedDescription:
                normalisedDescription.remove(name)
                collection = libraries[i]
    return collection, normalisedDescription
            
            
query = 'change the dimensions of an array numpy'
print('Stemming: ',normalise(query,stem = True))
print('Lemmatization: ', normalise(query,lemma= True))
print('Synonom Replacement: ',normalise(query,synon = True))

libraryCheck(normalise(query))

