text = "python is a good language. c# also is a good language"
lenght = len(text)

letter_a = 0

for x in text: 
    if x=='a':
        letter_a +=1
        
print (f"the number of the letter a is {letter_a}.")