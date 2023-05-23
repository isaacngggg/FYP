import nltk
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


print (normalise('Find indices where elements should be inserted to maintain order'))