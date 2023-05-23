import numpy as np

arr = np.array(['zero', 'three','1', 'six','two'])

score = np.array([0,3,1,6,2])

sorted = np.argsort(-score)

print (sorted[:3])

print (arr[sorted[:3]].tolist())