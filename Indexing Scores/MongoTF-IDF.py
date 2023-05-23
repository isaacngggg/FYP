from pymongo import MongoClient
import numpy as np

client = MongoClient('mongodb://localhost:27017/')
db = client['scrapped-function']
collection = db['all']
projection = {'description': 1}
cursor = collection.find({}, projection)


corpus = []
for document in cursor:
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

tokenized_corpus = []
for doc in corpus: 
    tokenized_corpus += [normalise (doc)]
    print (doc)
    
from sklearn.feature_extraction.text import TfidfVectorizer


    
vectorizer = TfidfVectorizer()

# Fit and transform the documents to calculate TF-IDF scores
tfidf_matrix = vectorizer.fit_transform(tokenized_corpus)

# Get the feature names (terms)
terms = vectorizer.get_feature_names()

# Loop through the documents and calculate the TF-IDF scores
for i, document in enumerate(tokenized_corpus):
    feature_index = tfidf_matrix[i, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])
    for term, score in [(terms[i], score) for (i, score) in tfidf_scores]:
        print(f"Term: {term}, TF-IDF score: {score}")