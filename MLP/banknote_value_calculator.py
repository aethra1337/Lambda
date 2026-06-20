def calculate_total_value(thickness, height_m, note_value, multiplier):
    """
    Calculates the total monetary value based on stack height.
    """
    # Convert height from meters to millimeters
    height_mm = height_m * 1000
    
    # Calculate how many banknotes are in that height
    number_of_banknotes = round(height_mm / thickness)
    
    # Final calculation (banknotes * value * your specific multiplier)
    total_result = number_of_banknotes * note_value * multiplier
    
    return round(total_result)

# --- How to use the function ---
thickness_input = 0.11
height_input = 1 # 1 meter
note_input = 1000
multiplier_input = 1

final_value = calculate_total_value(thickness_input, height_input, note_input, multiplier_input)

print(f"The final calculated value is: {final_value:,}")