
n = int(input("number of corners:"))

result = n * (n - 3) // 2

if n < 3:
    print(f"A polygon must have at least three sides")
    
else:
    print(f"A polygon with {n} sides has a total of {result} diagonals. ")