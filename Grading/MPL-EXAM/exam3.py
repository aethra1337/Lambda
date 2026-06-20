import random
import matplotlib.pyplot as plt

# X axis: months list
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Y axis: 12 random integers between 0 and 10
y_values = [random.randint(0, 10) for _ in range(12)]

# creating line chart
plt.plot(months, y_values, marker='o', linestyle='-', color='r')

plt.xticks(ticks=range(12), labels=months)

plt.xlabel("Months")
plt.ylabel("Random Values")
plt.title("Line Chart with 12 Random Values by Month")

plt.show()