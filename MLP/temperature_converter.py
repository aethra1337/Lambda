# 1. Ask the user for their choice
print("--- Temperature Converter ---")
print("1. Celsius to Fahrenheit")
print("2. Fahrenheit to Celsius")
choice = input("Select an option (1 or 2): ")

# 2. Process based on the selection
if choice == "1":
    # Celsius to Fahrenheit
    celsius = float(input("Enter degree in Celsius: "))
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C is equal to {fahrenheit:.2f}°F")

elif choice == "2":
    # Fahrenheit to Celsius
    fahrenheit = float(input("Enter degree in Fahrenheit: "))
    celsius = (fahrenheit - 32) * 5/9
    print(f"{fahrenheit}°F is equal to {celsius:.2f}°C")

else:
    print("Invalid selection. Please run the program again and choose 1 or 2.")