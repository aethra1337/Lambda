import random
import matplotlib.pyplot as plt

# X : months list
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Y : 12 random integers between 0 and 10
y_values = [random.randint(0, 10) for _ in range(12)]


plt.barh(range(12), y_values, color='r')

plt.yticks(ticks=range(12), labels=months)

# swapping integers y and x 
plt.xlabel("Random Values")
plt.ylabel("Months")
plt.title("Horizontal Bar Chart with 12 Random Values by Month")

plt.show()