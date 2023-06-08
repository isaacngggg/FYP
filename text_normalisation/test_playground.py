import numpy as np
import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(-10, 10, 100)

# Define the function for the trend line
def trend_line(x):
    return (2 * x) / (x**2 + 1)

# Calculate y values using the trend line function
y = trend_line(x)

# Plot the trend line
plt.plot(x, y, label='Trend Line')

# Set y-asymptotes at y = 0 and y = 2
plt.axhline(y=0, color='red', linestyle='--', label='y = 0')
plt.axhline(y=2, color='blue', linestyle='--', label='y = 2')

# Add labels and legend
plt.xlabel('x')
plt.ylabel('y')
plt.legend()

# Show the plot
plt.show()
