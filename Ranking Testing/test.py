
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

#%%
import matplotlib.pyplot as plt
import numpy as np

# Create the figure and the first axis
fig, ax1 = plt.subplots()

# Generate some example data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.exp(x)

# Plot the first dataset on the first axis
ax1.plot(x, y1, color='blue', label='Y1')
ax1.set_xlabel('X')
ax1.set_ylabel('Y1', color='blue')

# Create the second axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot the second dataset on the second axis
ax2.plot(x, y2, color='red', label='Y2')
ax2.set_ylabel('Y2', color='red')

# Create the third axis sharing the same x-axis
ax3 = ax1.twinx()

# Offset the third axis
ax3.spines['right'].set_position(('outward', 60))

# Plot the third dataset on the third axis
ax3.plot(x, y3, color='green', label='Y3')
ax3.set_ylabel('Y3', color='green')

# Display the legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3)

# Show the plot
plt.show()
