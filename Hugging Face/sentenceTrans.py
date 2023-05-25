from sentence_transformers import SentenceTransformer, util

sentences = ["I'm upset","I am sad", "I'm full of sadness"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)


for i in range (0,10):
    print (util.pytorch_cos_sim(embedding_1, embedding_2))
