import numpy as np

arr = np.array(['zero', 'three','1', 'six','two'])

sumRanks_bs = np.array([])

sumRanks_bs.reshape(5,0)

score = np.array([0,3,1,6,2])
score2 = np.array([0,3,1,6,2])

sorted = np.argsort(-score)

print (sorted[:3])

print (arr[sorted[:3]].tolist())


b_linspace = np.linspace(0.5,1,5)
ranksMat = np.array(b_linspace).reshape(1,len(b_linspace))
ranksMat = np.append(ranksMat,score.reshape(1,len(b_linspace)),0)
print(ranksMat)

ranksMat += score.reshape(5,1)

ranksMat += score2.reshape(5,1)

print (ranksMat)

print (np.concatenate((score.reshape(len(score),1),score2.reshape(len(score),1)),1))


#%%
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(-5, 5, 100)  # Values for parameter 1
y = np.linspace(-5, 5, 100)  # Values for parameter 2

# Create a meshgrid from the two parameters
X, Y = np.meshgrid(x, y)

# Calculate the Z values based on the two parameters
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# Add labels and title
ax.set_xlabel('Parameter 1')
ax.set_ylabel('Parameter 2')
ax.set_zlabel('Z')
ax.set_title('3D Plot with Varying Parameters')

# Display the plot
plt.show()

