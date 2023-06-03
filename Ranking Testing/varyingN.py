#%%
import numpy as np
import pandas as pd
import string as str
import time
import matplotlib.pyplot as plt
from testingFuncs import  timeStart, timeSince, getBM25Arrays,queryBERT

#%%

df = pd.read_csv('data_highQuality.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])

#%%
df = pd.read_csv('data_combined.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])

#%%
df = pd.read_csv('data_lowQuality.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])

#%%
#n_linspace = np.arange(50,1000,50)

# n_linspace = [30,35,40,45,50,60,75,100,150,200,300,400,800,1000]
#n_linspace = [800,1000]
n_linspace = [20,25,30,35,40,50,60,75,80,90,100,150,180,200,250,275,300,350,400,500,600,700,800]

#n_linspace = [20,25,30,35]

n_linspace = np.flip(n_linspace)

avBertRanksArr = []
avTimeArr = []
avBertTimeArr = []
avBm25TimeArr =[]
avBM25RankArr = []

TimeMat = []
BertTimeMat = []
Bm25TimeMat =[]
BertRanksMat = []
BM25RankMat = []
belowNMat = []
count = 0
for n in n_linspace:
    overallLapseArr = []
    bertTimeArr = []
    bm25TimeArr = []
    BM25RankArr = []
    BERTRankArr = []
    print ("N  = ",n)
    belowNIndex = []
    for j in range (0,len(queries)):
        start = timeStart()
        topN_titles,topN_Des, BM25Rank = getBM25Arrays(queries[j],funcs[j], n = n,normalMethod='stem',b = 0.75,k1 = 1.5)
        BMTime = timeSince(start)
        belowN = 0
        
        if funcs[j] in topN_titles:
            scoreBERTlist,bertTime = queryBERT(queries[j],topN_Des)
            scoreBERT = np.array(scoreBERTlist)
            sortedIndices = np.argsort(-scoreBERT)
            sortedTitles = [topN_titles[i] for i in sortedIndices]
            sortedNormDes = [topN_Des[i] for i in sortedIndices]
            BERTRank = [i for i, value in enumerate(sortedTitles) if value == funcs[j]]
            overallLapse = timeSince(start)
            BM25RankArr.append(BM25Rank)
            BERTRankArr = np.append(BERTRankArr,BERTRank) 
            overallLapseArr.append(overallLapse)
            bertTimeArr.append(bertTime)
            bm25TimeArr.append(BMTime)
            print ('Lapse Time',overallLapse)
        else:
            BM25RankArr.append(BM25Rank)
            bm25TimeArr.append(BMTime)
            BERTRankArr = np.append(BERTRankArr,BM25Rank)
            overallLapseArr.append(np.average(overallLapseArr))
            bertTimeArr.append(np.average(bertTimeArr))
            belowN += 1
            belowNIndex.append(j)
        print('Bert Array: ' ,BERTRankArr)
        time.sleep(1)
        
    print (belowNIndex)  
    avTimeArr.append(np.average(overallLapseArr))
    avBertTimeArr.append(np.average(bertTimeArr))
    avBm25TimeArr.append(np.average(bm25TimeArr))
    avBertRanksArr.append(np.average(BERTRankArr))
    avBM25RankArr.append(np.average(BM25Rank))
    
    TimeMat += [overallLapseArr]
    BertTimeMat += [bertTimeArr]
    Bm25TimeMat += [bm25TimeArr]
    BertRanksMat += [BERTRankArr]
    BM25RankMat += [BM25Rank]
    belowNMat.append(belowNIndex)
    
    count += 1
    
    print ('Bert time Per Query:',bertTimeArr)
    print ('Bert rank Per Query:',BERTRankArr)
    print (f'--------------_Completed {count/len(n_linspace)*100}%_----------------')

#%%
## get rid of arrays that doesn't fit inside the initial N
TimeMat_c = np.delete(TimeMat, belowNMat[0], axis=1)
BertTimeMat_c = np.delete(BertTimeMat, belowNMat[0], axis=1)
BertRanksMat_c = np.delete(BertRanksMat, belowNMat[0], axis=1)

avTime = np.mean (TimeMat_c,axis=1)
avTime_bert = np.mean (BertTimeMat_c,axis=1)
avRanks = np.mean (BertRanksMat_c,axis=1)


#%%
## PLot the average 
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(n_linspace, avRanks, color='tab:red',label='Average Rank')
ax2 = ax1.twinx()
ax2.plot(n_linspace, TimeMat_c, color='lightblue')
ax2.plot(n_linspace, avTime, color='blue', label='Average Overall Time')
ax2.plot(n_linspace, avBm25TimeArr, color='green',label='Average BM25')
ax2.plot(n_linspace, BertTimeMat_c, color='grey')
ax2.plot(n_linspace, avTime_bert, color='purple',label='Average Bert Time(s)')


ax2.legend(loc='lower right')

ax1.set_xlabel('N-Value')
ax1.set_ylabel('Average Ranks', color='tab:red')
ax2.set_ylabel('Average OverAllLapse Time(s)', color='tab:blue')
plt.title('The effect of N on accuracy and speed')

plt.show()

#%%
## plotting individual queries
avRanks = np.mean (BertRanksMat,axis=1)
avTime = np.mean (TimeMat,axis=1)

BertRanksMat = np.array(BertRanksMat)
TimeMat = np.array(TimeMat)

print (len(queries))
for i in range(0,len(queries)):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(n_linspace, avRanks, color='grey',label='Average Rank')
    label = f"Rank for the query: {queries[i]}"
    ax1.plot(n_linspace, BertRanksMat[:,i], color='red',label=label)
    ax2 = ax1.twinx()
    ax2.plot(n_linspace, avTime, color='grey', label='Average Overall Time')
    label = f"Time for query: {queries[i]}"
    ax2.plot(n_linspace, TimeMat[:,i], color='green',label= label )
    ax2.legend(loc='lower right')

    ax1.set_xlabel('N-Value')
    ax1.set_ylabel('Average Ranks', color='tab:red')
    ax2.set_ylabel('Average OverAllLapse Time(s)', color='tab:blue')
    plt.title(f'Accuracy and speed for the query: {queries[i]}')


#%%
noOfMisses = []
for i in range(0,len(belowNMat)):
    noOfMisses.append(len(belowNMat[i]))
    
print (noOfMisses)
plt.plot(n_linspace , noOfMisses)
plt.xlabel('N')
plt.ylabel('Number of misses')
plt.title('Number of misses by BM25')
