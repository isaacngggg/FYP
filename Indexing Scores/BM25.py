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

# Define a corpus of documents
corpus = [
    "This is the first document",
    "This document is the second document",
    "And this is the third one",
    "Is this the first document?"
] 
tokenized_corpus = []
for doc in corpus: 
    tokenized_corpus += [normalise (doc)]
    print (doc)

print (tokenized_corpus)
    
# Tokenize the corpus
#tokenized_corpus = [doc.split() for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

print (bm25)

# Define a query
query = "first document"

tokenized_query = normalise(query)

doc_scores = bm25.get_scores(tokenized_query)
# array([0.        , 0.93729472, 0.        ])
# Get document scores for the query using BM25

# ['It is quite windy in London']
print (doc_scores)
print (bm25.get_top_n(tokenized_query, corpus, n=1))
