import nltk

import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text

def normalise (description):
    tokens = word_tokenize(description)
    tokens_without_punctuation = [token for token in tokens if not any(char in string.punctuation for char in token)]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in tokens_without_punctuation]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in stemmed_words if word.lower() not in stop_words]
    normalisedDescription = filtered_words
    return normalisedDescription

def normalise_wlem (description):
    tokens = word_tokenize(description)
    tokens_without_punctuation = [token for token in tokens if not any(char in string.punctuation for char in token)]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens_without_punctuation]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in lemmatized_tokens]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in stemmed_words if word.lower() not in stop_words]
    normalisedDescription = filtered_words
    return normalisedDescription

def replace_synonyms(tokens):
    
    # Iterate over each token
    replaced_tokens = []
    noOfSynsets = []
    for token in tokens:
        # Get the synsets (synonymous sets) for the token
        synsets = wordnet.synsets(token)
        noOfSynsets += [len(synsets)]
        if synsets:
            # Get the first synset
            first_synset = synsets[0]
            
            # Get the lemma names (synonymous words) for the synset
            lemma_names = first_synset.lemma_names()
            
            if lemma_names:
                # Replace the token with the first lemma name
                replaced_token = lemma_names[0]
                replaced_tokens.append(replaced_token)
            else:
                replaced_tokens.append(token)
        else:
            replaced_tokens.append(token)
    
    return replaced_tokens

def normalise_wLem_wSyn (description):
    tokens = word_tokenize(description)
    tokens_without_punctuation = [token for token in tokens if not any(char in string.punctuation for char in token)]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens_without_punctuation]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in lemmatized_tokens if word.lower() not in stop_words]
    normalisedDescription = replace_synonyms(filtered_words)
    return normalisedDescription

print (normalise('Find indices , index where maximum elements should be inserted to maintain order'))
print (normalise_wlem('Find indices , index where maximum elements should be inserted to maintain order'))
print (normalise_wLem_wSyn('Find indices , index where maximum elements should be inserted to maintain order'))