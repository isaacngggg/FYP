
import numpy as np

import matplotlib.pyplot as plt
n_linspace = [1,2,3]
belowNMat = [
    [0,1,4],
    [0,1,4],
    [0,1]
]
noOfMisses = []
for i in range(0,len(belowNMat)):
    print(len(belowNMat[i]))
    noOfMisses.append(len(belowNMat[i]))
    
print(noOfMisses)

plt.bar(n_linspace, noOfMisses)
plt.xlabel('N values')
plt.ylabel('Number of BM25 failures')
plt.title('Number of BM25 failures')
plt.show()