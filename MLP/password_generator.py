import random
import string

lenght = int(input("Lenght: "))
choice = input("Uppercase, Lowercase, Number, Symbol (e.g: 1 is yes, 0 is no): ")

groups = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]

pool = "".join(groups[i] for i in range(4) if choice[i] == "1")

print("Password:", "".join(random.choices(pool, k=lenght)))