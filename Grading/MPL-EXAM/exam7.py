import random

# 1. generate 12 random numbers and add them to the list (between 1-100 )
numbers = [random.randint(1, 100) for _ in range(12)]

# 2. calcs
total = sum(numbers) / len(numbers)
biggest = max(numbers)
smallest = min(numbers)

# 3. print the results
print(f"Numbers List: {numbers}")
print(f"Total: {total:.2f}")
print(f"Biggest value is : {biggest}")
print(f"Smallest valueis : {smallest}")
