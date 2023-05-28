from nltk.corpus import wordnet

def replace_synonyms(text):
    # Tokenize the text
    tokens = text.split()
    
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
    
    # Join the replaced tokens back into a normalized text
    normalized_text = ' '.join(replaced_tokens)
    
    return replaced_tokens,tokens,noOfSynsets

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

print (replace_synonyms('Find indices index where maximum elements should be inserted to maintain order'))