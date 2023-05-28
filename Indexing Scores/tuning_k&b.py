#%%
import pandas as pd
import numpy as np
from MongoBM25 import normalise,fetchMongobyID,printtop_n,printDoc,fetchAllMongo
from rank_bm25 import BM25Okapi
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('data.csv')
queries = np.array(df["query"])
func = np.array(df["function"])


sumRanks_bs = []
ranks = []
tokenized_corpus, corpus, IDs, titles = fetchAllMongo()

n = 10

k1_linspace = np.linspace(1,10,n)
b_linspace = np.linspace(0,1,n)

k1grid, bgrid = np.meshgrid(k1_linspace, b_linspace)
Xgrid = np.array([k1grid, bgrid]).reshape([2,n*n]).T

def getSumofRanks (k1,b,tokenized_corpus, corpus, IDs, titles):
    rankings = []
    actualDescriptions = []
    fetchedTitles = []
    for j in range (0, len(queries)):
        query = queries[j]
        normalised_query = normalise(query,synon=False)
        
        bm25 = BM25Okapi(tokenized_corpus,b=b,k1=k1)
        scoresBM25 = np.array(bm25.get_scores(normalised_query))  
        sortedScores = np.sort(-scoresBM25)
        sortedBM25Arr = np.argsort(-scoresBM25)

        indices = [i for i, value in enumerate(titles) if value == func[j]]
        rank = [i for i, value in enumerate(sortedScores) if value == -scoresBM25[indices]]

        rankings += [rank[0]]
        actualDescriptions += [corpus[indices[0]]]
        fetchedTitles += [titles[indices[0]]]

    return np.sum(rankings)

for i in range (0,len(Xgrid[:,0])):
    ranks += [getSumofRanks(Xgrid[i,0],Xgrid[i,1],tokenized_corpus, corpus, IDs, titles)]
    
ranks = np.array(ranks).reshape(n,n)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(k1grid, bgrid, ranks)

ax.set_xlabel('k1')
ax.set_ylabel('b')
ax.set_zlabel('Sum of Ranks')
#%%
print (np.min(ranks))
# %%
