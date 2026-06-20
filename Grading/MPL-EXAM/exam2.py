import random
import matplotlib.pyplot as plt

# X: numbers from 1 to 12
x_values = list(range(1, 13))

# Y: 12 random integers between 0 and 10
y_values = [random.randint(0, 10) for _ in range(12)]

plt.plot(x_values, y_values, marker='o')

plt.xlabel("Index")
plt.ylabel("Random Values")
plt.title("12 Random Lines 0-100")

plt.show()