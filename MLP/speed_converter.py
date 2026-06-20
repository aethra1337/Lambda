# Function to convert Speed
def speed_converter():
    print("Basit Hız Çevirimi")
    
    try:
        # Ask the user for Kilometers
        kmh = float(input("Hızı giriniz 'km/h' cinsinde: "))
        
        # 1 km is close to  0.621371 miles
        donusum = 0.621371
        
        # Calculate Miles per Hour
        mph = kmh * donusum
        
        # Display the result to 2 decimal places
        print(f"Sonuç: {kmh} km/h is eşittir {mph:.2f} mph")
        
    except ValueError:
        # Error handling 
        print("Hatalı giriş. Lütfen numerik sonuçlar giriniz")

# Run the function
speed_converter()