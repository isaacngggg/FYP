#%%
from testingFuncs import getRanksArr,fetchAllMongo,normalise
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
df = pd.read_csv('data.csv')

#%%
## loading in low quality data
df = pd.read_csv('data_lowQuality.csv')

#%%
df = pd.read_csv('data_combined.csv')
#%%
queries = np.array(df["query"])
funcs = np.array(df["function"])


#%%
methodsTitle = ['Stemming','Lemmatization','Synonym Replacement']
methods = ['stem','lem','synon']

ranks = [[getRanksArr(queries,funcs,normalMethod=method)] for method in methods]

avRanks = [np.average(r) for r in ranks]

plt.bar(methodsTitle, avRanks)
plt.xlabel('Normalisation Methods')
plt.ylabel('Average Ranking')
plt.title('Initial Normalisation Methods Average Ranking')


#%%
bar_height = 0.25
index = np.arange(len(queries))
plt.barh(index + bar_height, ranks[0][0], height=bar_height, label=methodsTitle[0])
plt.barh(index , ranks[1][0], height=bar_height, label=methodsTitle[1])
plt.barh(index - bar_height, ranks[2][0], height=bar_height, label=methodsTitle[2])

plt.yticks(index, funcs)
plt.xlabel('Ranks')
plt.ylabel('Queries')
plt.legend()
plt.title('Ranks per query under different normalisation methods')


#%%
titleAna = "numpy."+ input ("Title of the numpy function to be analysed")
ids,titles,des,stemDes,lemDes,stemLemDes,synonDes = fetchAllMongo()
synPrint = 0
for i in range(len(titles)):
    if titles[i] == titleAna :
        actualDes = des [i]
print (f'Analysis title: {titleAna}\n')
print (f'Scrapped description: {actualDes}')
print('Stemming: ',normalise(actualDes,stem = True))
print('Lemmatization: ', normalise(actualDes,lemma= True))
print('Synonym replacement: ',normalise(actualDes,synon = True,printSynon=synPrint))

for i in range(len(queries)):
    if funcs[i] == titleAna :
        query = queries[i]
        
print (f'\n\nUser query: {query}\n')
print('Stemming: ',normalise(query,stem = True))
print('Lemmatization: ', normalise(query,lemma= True))
print('Synonym replacement: ',normalise(query,synon = True,printSynon=synPrint))

