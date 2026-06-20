import random
import matplotlib.pyplot as plt

# X axis: numbers from 1 to 12
x_values = list(range(1, 13))

# Y axis: 12 random integers between 0 and 10
y_values = [random.randint(0, 10) for _ in range(12)]

# Create bar chart
plt.bar(x_values, y_values)

plt.xlabel("Index")
plt.ylabel("Random Values")
plt.title("Bar Chart with 12 Random Values")

plt.show()