#%%
import numpy as np
import pandas as pd
import string as str
import time
import matplotlib.pyplot as plt
from testingFuncs import  timeStart, timeSince, getBM25Arrays,queryBERT

#%%
df = pd.read_csv('data.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])
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
#n_linspace = np.arange(20,1000,50)

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
        else:
            BM25RankArr.append(BM25Rank)
            bm25TimeArr.append(BMTime)
            BERTRankArr = np.append(BERTRankArr,BM25Rank)
            overallLapseArr.append(np.average(overallLapseArr))
            bertTimeArr.append(np.average(bertTimeArr))
            belowN += 1
            belowNIndex.append(j)
        print('Bert Array: ' ,BERTRankArr)
        #time.sleep(1)
        
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
    #time.sleep(3)
    
#%% Initial with just time
avTime = np.mean (TimeMat,axis=1)
avTime_bert = np.mean (BertTimeMat,axis=1)
avRanks = np.mean (BertRanksMat,axis=1)

timeError = np.std(TimeMat,axis=1) / np.sqrt(len(TimeMat))

plt.scatter(n_linspace,avTime_bert,label = 'Average Bert Time')
plt.errorbar(n_linspace,avTime_bert,yerr=timeError,fmt = 'o',capsize=4)
plt.xlabel('N value')
plt.ylabel('Time(s)')
plt.title('Bert querying time vs N')

#%% Initial shit
avTime = np.mean (TimeMat,axis=1)
avTime_bert = np.mean (BertTimeMat,axis=1)
avRanks = np.mean (BertRanksMat,axis=1)

timeError = np.std(TimeMat,axis=1) / np.sqrt(len(TimeMat))

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(n_linspace, avRanks, color='tab:red',label='Average Rank')
ax2 = ax1.twinx()
ax2.scatter(n_linspace, avTime, color='blue', label='Average Overall Time')
ax2.errorbar(n_linspace,avTime,yerr=timeError,fmt = 'o',capsize=4)
ax2.scatter(n_linspace, avBm25TimeArr, color='green',label='Average BM25')
ax2.scatter(n_linspace, avTime_bert, color='purple',label='Average Bert Time(s)')


ax2.legend(loc='lower right')

ax1.set_xlabel('N-Value')
ax1.set_ylabel('Average Ranks', color='tab:red')
ax2.set_ylabel('Average OverAllLapse Time(s)', color='tab:blue')
plt.title('The effect of N on accuracy and speed')

plt.show()


#%% plotting individual queries
avRanks = np.mean (BertRanksMat,axis=1)
avTime = np.mean (TimeMat,axis=1)

BertRanksMat = np.array(BertRanksMat)
TimeMat = np.array(TimeMat)

print (len(queries))
for i in range(0,len(queries)):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.scatter(n_linspace, avRanks, color='grey',label='Average Rank')
    label = f"Rank for the query: {queries[i]}"
    ax1.scatter(n_linspace, BertRanksMat[:,i], color='red',label=label)
    ax2 = ax1.twinx()
    ax2.scatter(n_linspace, avTime, color='grey', label='Average Overall Time')
    label = f"Time for query: {queries[i]}"
    ax2.scatter(n_linspace, TimeMat[:,i], color='green',label= label )
    ax2.legend(loc='lower right')

    ax1.set_xlabel('N-Value')
    ax1.set_ylabel('Average Ranks', color='tab:red')
    ax2.set_ylabel('Average OverAllLapse Time(s)', color='tab:blue')
    plt.title(f'Accuracy and speed for the query: {queries[i]}')





#%% Plotting the reduction in rank instead of the average rank

rankReduction = np.array(BM25RankMat) - np.array(BertRanksMat)

avRankReduction = np.mean (rankReduction,axis=1)
avRanks = np.mean (BertRanksMat,axis=1)

avTime = np.nanmean (TimeMat,axis=1)
avBM25Time = np.nanmean (Bm25TimeMat,axis = 1)
avBERTTime = np.nanmean (BertTimeMat,axis = 1)

timeError = np.std(BertTimeMat,axis=1) / np.sqrt(len(BertTimeMat))

from scipy import stats
z_scores = np.abs(stats.zscore(avTime))
print (z_scores)
outlier_threshold = 2
filtered_nt = n_linspace[z_scores <= outlier_threshold]
filtered_t = avBERTTime[z_scores <= outlier_threshold]
filtered_bm = avBM25Time[z_scores <= outlier_threshold]
filtered_o = avTime[z_scores <= outlier_threshold]
filter_er = timeError[z_scores <= outlier_threshold]

r = filtered_bm - np.mean(filtered_bm)

bert_arr = filtered_t - r
o_arr = filtered_o - r


n_trend = np.arange(20,850,50)

coefficients = np.polyfit(filtered_nt,bert_arr,1)
trendlinet = np.poly1d(coefficients)
print (np.mean(filtered_bm))

decision_ranks = 20
decision_M = 4

fs = 12
ts = 20

# plt.scatter(filtered_n,filtered_t,label = 'Average BERT runtime')
# plt.scatter(n_linspace,avTime,color='grey',label = 'Average overall runtime')
# plt.errorbar(n_linspace,avBERTTime,yerr=timeError,fmt = 'o',capsize=4)
#%% Plotting time
plt.scatter(n_linspace,avBM25Time,color='green',label = 'Average BM25 runtime')

plt.ylim(0,1.2)

plt.errorbar(filtered_nt,bert_arr,yerr=filter_er,fmt = 'o',capsize=4)
plt.scatter(filtered_nt,o_arr,color='dimgray',label = 'Average overall runtime without Noise')
plt.scatter(filtered_nt,bert_arr,color='navy',label = 'Average overall runtime without Noise')
plt.plot(n_trend, trendlinet(n_trend), color='cornflowerblue', label='Estimated average BERT runtime trend line')

plt.legend()
plt.xlabel('N value',fontsize = fs)
plt.ylabel('Average Runtime(s)',fontsize = fs)
plt.title ("Average runtime of BM25, BERT & the overall program across N")


#%% Average Rank with Number of misses
from scipy import stats

eliminate_n = n_linspace[:]
eliminate_r = avRanks[:]

z_scores = np.abs(stats.zscore(eliminate_r))
print (z_scores)
outlier_threshold = 3

filtered_n = eliminate_n[z_scores <= outlier_threshold]
filtered_r = eliminate_r[z_scores <= outlier_threshold]


n_trend = np.arange(20,850,50)

coefficients = np.polyfit(eliminate_n,eliminate_r,3)
trendliner = np.poly1d(coefficients)
print (z_scores)



noOfMisses = []
for i in range(0,len(belowNMat)):
    noOfMisses.append(len(belowNMat[i]))


fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.scatter(n_linspace, avRanks, color='tab:red',label='Average rank')
ax1.plot(n_trend,trendliner(n_trend),color = 'tab:red',label = 'Trend line for average rank' )



ax1.axhline(y=decision_ranks,color = "r",linestyle = "--")
ax1.set_ylim(0,125)
ax2 = ax1.twinx()
ax2.axhline(y=decision_M,color = "g",linestyle = "--")
ax2.bar(n_linspace,noOfMisses,color = 'darkgreen',label = 'M - Number of queries not in dense layer',width=5)
ax1.text(550, decision_ranks, f'Average of rank {decision_ranks}', color='r', ha='right', va='bottom')
ax2.text(800, decision_M, '85%% success rate', color='g', ha='right', va='bottom')
ax1.set_xlabel('N-Value',fontsize = fs)
ax1.set_ylabel('Average ranking', color='tab:red',fontsize = fs)
ax2.set_ylabel('Number of queries not in dense layer', color='tab:green',fontsize = fs)
plt.title('The effect of N on accuracy')

plt.show()


#%% Average Rank Reduction with Number of misses
from scipy import stats

eliminate_n = n_linspace[3:]
eliminate_r = avRanks[3:]

z_scores = np.abs(stats.zscore(eliminate_r))
print (z_scores)
outlier_threshold = 3

filtered_n = eliminate_n[z_scores <= outlier_threshold]
filtered_r = eliminate_r[z_scores <= outlier_threshold]


n_trend = np.arange(20,800,50)

coefficients = np.polyfit(eliminate_n,eliminate_r,1)
trendline = np.poly1d(coefficients)
print (z_scores)



noOfMisses = []
for i in range(0,len(belowNMat)):
    noOfMisses.append(len(belowNMat[i]))
    

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.scatter(n_linspace, avRankReduction, color='tab:red',label='Average rank')
#ax1.plot(n_trend,trendline(n_trend),color = 'tab:red',label = 'Trend line for average rank' )

ax2 = ax1.twinx()
ax2.bar(n_linspace,noOfMisses,color = 'darkgreen',label = 'Number of queries not in dense layer',width=5)


ax1.set_xlabel('N-Value')
ax1.set_ylabel('Average ranking', color='tab:red')
ax2.set_ylabel('Number of queries not in dense layer', color='tab:green')
plt.title('The effect of N on accuracy')

plt.show()


#%% Plot average time vs average rank

decision_ranks = 40

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.axhline(y=decision_ranks,color = "r",linestyle = "--")
ax1.axvline(x=515,color = "grey",linestyle = "--")

ax1.scatter(n_linspace, avRanks, color='tab:red',label='Average rank')
ax1.text(850, decision_ranks, f'Average of rank {decision_ranks} & a success rate 85%', color='r', ha='right', va='bottom')
ax1.plot(n_trend,trendliner(n_trend),color = 'tab:red',label = 'Trend line for average rank' )
ax1.set_ylim(0,125)
ax2 = ax1.twinx()
axh2=0.47
ax2.axhline(y=axh2,color = "b",linestyle = "--")
ax2.text(850, axh2, f'Estimated Runtime of {axh2}s', color='b', ha='right', va='bottom')
ax2.set_ylim(0.3,0.6)
ax2.errorbar(filtered_nt,bert_arr,yerr=filter_er,fmt = 'o',capsize=4)
ax2.scatter(filtered_nt,bert_arr,color='navy',label = 'Average overall runtime without Noise')
ax2.plot(n_trend, trendlinet(n_trend), color='cornflowerblue', label='Estimated average BERT runtime trend line')
ax2.legend(loc='lower right')

ax1.set_xlabel('N-Value',fontsize = fs)
ax1.set_ylabel('Average Ranking', color='tab:red',fontsize = fs)
ax2.set_ylabel('Average Runtime(s)', color='tab:blue',fontsize = fs)


plt.title('The effect of N on accuracy and speed')

plt.show()
