# NUMBER GUESSING GAME

import random as a
num=a.randint(0,100)
print("=================================")
print(" Welcome to Number Guessing Game")
print("\n The numbers are between 1 and 100\n")

y=False
for i in range(0,10):
    x=int(input("guess the number:"))
    if x==num:
        print("you win, the number was",num)
        y=True
        break
    elif x>num:
        print("the num is lesser than your guess")
    else:
        print("the num is greater than your guess")
if y==False:
    print(f"better luck next time, the num was {num}")
    
