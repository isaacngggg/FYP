#%%
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from testingFuncs import  timeStart, timeSince, getBM25Arrays,queryBERT

df = pd.read_csv('data_cleaned.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])



#%%
n_linspace = np.arange(50,150,5)
avRanksArr = []
avTimeArr = []
avBertTimeArr = []
avBm25TimeArr =[]
for n in n_linspace:
    overallLapseArr = []
    bertTimeArr = []
    bm25TimeArr = []
    BM25RankArr = []
    BERTRankArr = []
    for j in range (0,len(queries)):
        start = timeStart()
        topN_titles,topN_Des, BM25Rank = getBM25Arrays(queries[j],funcs[j], n = n,normalMethod='stem',b = 0.75,k1 = 1.5)
        BMTime = timeSince(start)
        bertStart = timeStart()
        scoreBERT = np.array(queryBERT(queries[j],topN_Des))
        bertTime = timeSince(bertStart)
        sortedIndices = np.argsort(-scoreBERT)
        sortedTitles = [topN_titles[i] for i in sortedIndices]
        sortedNormDes = [topN_Des[i] for i in sortedIndices]
        BERTRank = [i for i, value in enumerate(sortedTitles) if value == funcs[j]]
        BM25RankArr += BM25Rank
        BERTRankArr += BERTRank
        overallLapse = timeSince(start)
        overallLapseArr += [overallLapse]
        bertTimeArr += [bertTime]
        bm25TimeArr += [BMTime]
        print ('Lapse Time',overallLapse)
    avBertTimeArr += [np.average(bertTimeArr)]
    avBm25TimeArr += [np.average(bm25TimeArr)]
    avRanksArr += [np.average(BERTRankArr)]
    avTimeArr += [np.average(overallLapseArr)]
    print ('Bert time Per Query:',bertTimeArr)
#%%

# Reverse N

n_linspace = np.flip(np.arange(40,240,20))
avRanksArr = []
avTimeArr = []
avBertTimeArr = []
avBm25TimeArr =[]
for n in n_linspace:
    overallLapseArr = []
    bertTimeArr = []
    bm25TimeArr = []
    BM25RankArr = []
    BERTRankArr = []
    for j in range (0,len(queries)):
        start = timeStart()
        topN_titles,topN_Des, BM25Rank = getBM25Arrays(queries[j],funcs[j], n = n,normalMethod='stem',b = 0.75,k1 = 1.5)
        BMTime = timeSince(start)
        bertStart = timeStart()
        scoreBERT = np.array(queryBERT(queries[j],topN_Des))
        bertTime = timeSince(bertStart)
        sortedIndices = np.argsort(-scoreBERT)
        sortedTitles = [topN_titles[i] for i in sortedIndices]
        sortedNormDes = [topN_Des[i] for i in sortedIndices]
        BERTRank = [i for i, value in enumerate(sortedTitles) if value == funcs[j]]
        BM25RankArr += BM25Rank
        BERTRankArr += BERTRank
        overallLapse = timeSince(start)
        overallLapseArr += [overallLapse]
        bertTimeArr += [bertTime]
        bm25TimeArr += [BMTime]
        print ('Lapse Time',overallLapse)
    avBertTimeArr += [np.average(bertTimeArr)]
    avBm25TimeArr += [np.average(bm25TimeArr)]
    avRanksArr += [np.average(BERTRankArr)]
    avTimeArr += [np.average(overallLapseArr)]
    print ('Bert time Per Query:',bertTimeArr)

#%%
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(n_linspace, avRanksArr, color='tab:red',label='Average Rank')
ax2 = ax1.twinx()
ax2.plot(n_linspace, avTimeArr, color='blue', label='Average Overall Time')
ax2.plot(n_linspace, avBm25TimeArr, color='green',label='Average BM25')
ax2.plot(n_linspace, avBertTimeArr, color='purple',label='Average Bert Time(s)')
ax2.legend(loc='lower right')

ax1.set_xlabel('N-Value')
ax1.set_ylabel('Average Ranks', color='tab:red')
ax2.set_ylabel('Average OverAllLapse Time(s)', color='tab:blue')
plt.title('The effect of N on accuracy and speed')

plt.show()
