#%%
from testingFuncs import getRanksArr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('data.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])

methods = ['stem','lem','stemLem','synon']
ranks = [[getRanksArr(queries,funcs,normalMethod=method)] for method in methods]

avRanks = [np.average(r) for r in ranks]

plt.bar(methods, avRanks)
plt.xlabel('Normalisation Methods')
plt.ylabel('Average Ranks')
plt.title('Average Ranks with Outliers')


#%%

plt.barh(funcs, ranks[0][0])
plt.xlabel('Queries')
plt.ylabel('Ranks')
#plt.xticks(rotation=70)

plt.title('Ranks with BM25 using Stemming')

#%%
ranks_woOutliers = [np.delete(r,11) for r in ranks]
avRanks = [np.average(r) for r in ranks]
print (ranks_woOutliers)
plt.bar(methods, avRanks)
plt.xlabel('Normalisation Methods')
plt.ylabel('Average Ranks')
plt.title('Average Ranks without Outliers')

