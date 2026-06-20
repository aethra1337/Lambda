# --- Mathematical Functions ---

def add(a, b):
    return a + b

def subtract(a, b):
    return b - a  # calculates the difference

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b if b != 0 else "Error: Division by zero"

def power(base, exponent):
    return base ** exponent

# --- Inputs ---
val_a = 8
val_b = 4

# --- Execution & Results ---
print(f"--- Results for {val_a} and {val_b} ---")
print(f"Add           : {add(val_a, val_b)}")
print(f"Subtract      : {subtract(val_a, val_b)}")
print(f"Multiply      : {multiply(val_a, val_b)}")
print(f"Divide        : {divide(val_a, val_b)}")

print(f"\n--- Power Operations ---")
print(f"{val_a}^{val_b} is  : {power(val_a, val_b)}")
print(f"{val_b}^{val_a} is  : {power(val_b, val_a)}")