import random as a
num = a.randint(1,100)
x = int(input("Enter any number: "))
while num!= x:
    if x < num:
        print("lower than answer")
        x = int(input("Enter number again: "))
    elif x > num:
        print("higher than answer")
        x = int(input("Enter number again: "))
    else:
      break
print("you guessed it right!!")
