#ROCK PAPER AND SCISSORS

import random as a
print("================================")
print("Welcome to Rock, Paper and Scissors \n The game is for 3 points")
com=0
user=0
while com<3 or user<3:
    z=["rock","paper","scissors"]
    x=a.randint(0,2)
    y=int(input("enter 1.rock, 2.paper or 3.scissors:"))-1
    if y not in [0,1,2]:
        print("try again")
    else:
        if y==x:
            print("the computer chose",z[x],"\n its a draw")
        elif y==0 and x==1 or y==1 and x==2 or y==2 and x==0:
            com+=1
            print("the computer chose",z[x],"\n point for com")
        else:
            user+=1
            print("the computer chose",z[x],"\n point for user")
if com==3:
    print("computer has won")
else:
    print("you won")
