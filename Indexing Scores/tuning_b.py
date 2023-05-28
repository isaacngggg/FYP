import pandas as pd
import numpy as np
from MongoBM25 import normalise,fetchMongobyID,printtop_n,printDoc,fetchAllMongo
from rank_bm25 import BM25Okapi
from matplotlib import pyplot as plot

df = pd.read_csv('data.csv')
queries = np.array(df["query"])
func = np.array(df["function"])


def scores_BM25Top_n (normalised_query,n = 50):
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.array(bm25.get_scores(normalised_query))
    return doc_scores


sumRanks_bs = []
ranksMat = []
tokenized_corpus, corpus, IDs, titles = fetchAllMongo()

# b = np.arange(0.75,1,0.05)

k1_linespace = np.linspace(1.5,3,5)
b_linspace = np.linspace(0.5,1,5)
ranksMat = np.zeros((1,len(queries)))
for b in b_linspace:
    rankings = []
    actualDescriptions = []
    fetchedTitles = []
    for j in range (0, len(queries)):
        query = queries[j]
        normalised_query = normalise(query)
        
        bm25 = BM25Okapi(tokenized_corpus,b=b)
        scoresBM25 = np.array(bm25.get_scores(normalised_query))
        
        
        sortedScores = np.sort(-scoresBM25)
        sortedBM25Arr = np.argsort(-scoresBM25)
        #printtop_n(sortedBM25Arr,IDs,n = 10)

        indices = [i for i, value in enumerate(titles) if value == func[j]]

        #print (scoresBM25[indices])

        rank = [i for i, value in enumerate(sortedScores) if value == -scoresBM25[indices]]

        rankings += [rank[0]]
        actualDescriptions += [corpus[indices[0]]]
        fetchedTitles += [titles[indices[0]]]
        # print (func[j],queries[j])
        #print (titles[indices[0]],corpus[indices[0]])
        # print (ranking[0])
    sumRanks_b = np.sum(rankings)
    #print (sumRanks_b)
    sumRanks_bs += [sumRanks_b]
    Ranks_bs_Arr = np.array(rankings)
    print (Ranks_bs_Arr.reshape(1,len(queries)))
    ranksMat = np.append(ranksMat,Ranks_bs_Arr.reshape(1,len(queries)),0)

#some real janky shit
ranksMat = ranksMat[1:]
print (sumRanks_bs)
plot.scatter(b_linspace,sumRanks_bs)
for i in range(0,len(queries)):
    plot.plot(b_linspace,ranksMat[:,i])
plot.show()




# print (rankings)

# def printAny(i):
#     print (fetchedTitles[i])
#     print (actualDescriptions[i])
#     #print (rankings[i])
#     print (queries[i])
    
# while (1):
#     desRank = int(input ("Which indices: "))
#     desRankIndex = [i for i, value in enumerate(rankings) if value == desRank]
#     printAny(desRankIndex[0])

