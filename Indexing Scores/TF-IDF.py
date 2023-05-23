from sklearn.feature_extraction.text import TfidfVectorizer

# Create a list of document texts from MongoDB
documents = [...]  # List of document texts retrieved from MongoDB

# Create an instance of TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the documents to calculate TF-IDF scores
tfidf_matrix = vectorizer.fit_transform(documents)

# Get the feature names (terms)
terms = vectorizer.get_feature_names()

# Loop through the documents and calculate the TF-IDF scores
for i, document in enumerate(documents):
    feature_index = tfidf_matrix[i, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])
    for term, score in [(terms[i], score) for (i, score) in tfidf_scores]:
        print(f"Term: {term}, TF-IDF score: {score}")