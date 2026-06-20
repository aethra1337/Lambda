import random
import matplotlib.pyplot as plt

# X : months list
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Y : 12 random integers between 0 and 10
y_values = [random.randint(0, 10) for _ in range(12)]


plt.bar(range(12), y_values, color='r')

# This maps the numbers 0-11 to month names correctly on X axis
plt.xticks(ticks=range(12), labels=months)

plt.xlabel("Months")
plt.ylabel("Random Values")
plt.title("Bar Chart with 12 Random Values by Month")

plt.show()