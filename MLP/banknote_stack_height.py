#inputs
banknote_thickness_mm = 0.11
target_money_amount = 1000000000
banknote_value = 100 #100, 50, etc.

#how many banknotes are needed
number_of_banknotes = target_money_amount / banknote_value

#calculate the total height in millimeters
total_height_mm = number_of_banknotes * banknote_thickness_mm

#convert millimeters to meters
total_height_m = total_height_mm / 1000

#outputs
print(f"To reach {target_money_amount:,} units:")
print(f"You need {int(number_of_banknotes):,} banknotes of {banknote_value} units.")
print(f"The total height of the stack will be: {total_height_m:.2f} meters.")