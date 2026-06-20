import random

output = [0,0,0,0,0,0,0,0,0,0,0]

for i in range(1000000):
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    result = dice1 + dice2
    output[result-2] +=1 
    #print(result, end=" ")
print("----------\n")    

for i in range(10):
    print(f"{i+2} --> {round(100*output[i]/1000000,1)}%")