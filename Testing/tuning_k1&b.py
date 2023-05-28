#%%
import pandas as pd
import numpy as np
from testingFuncs import getRanksArr
from rank_bm25 import BM25Okapi
from matplotlib import pyplot as plt

df = pd.read_csv('data.csv')
queries = np.array(df["query"])
funcs = np.array(df["function"])


sumRanks_bs = []
avRanks = []

def genSampleGrid (n):
    k1_linspace = np.linspace(0.1,2,n)
    b_linspace = np.linspace(0.1,1,n)
    k1grid, bgrid = np.meshgrid(k1_linspace, b_linspace)
    Xgrid = np.array([k1grid, bgrid]).reshape([2,n*n]).T
    return Xgrid,k1grid,bgrid

n = 30

Xgrid,k1grid,bgrid = genSampleGrid(n)

for i in range (0,len(Xgrid[:,0])):
    avRanks += [np.average(getRanksArr(queries,funcs,normalMethod = 'stem', k1 = Xgrid[i,0],b = Xgrid[i,1]))]
    
ranksMat = np.array(avRanks).reshape(n,n)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(k1grid, bgrid, ranksMat)
ax.set_xlabel('k1')
ax.set_ylabel('b')
ax.set_zlabel('Sum of Ranks')

plt.show()
#%%
plt.contourf(k1grid, bgrid, ranksMat, cmap='viridis')
plt.colorbar()

# Add labels and title
plt.xlabel('k1')
plt.ylabel('b')
plt.title('2D Contour Plot')

# Display the plot
plt.show()


#%%
min_index = np.unravel_index(ranksMat.argmin(), ranksMat.shape)
print(min_index)
print (np.min(ranksMat))
print ('k1',k1grid[min_index])
print ('b',bgrid[min_index])