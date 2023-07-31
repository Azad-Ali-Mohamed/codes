import time

print ("Hello Time to play hangman!")
time.sleep(5)

print ("Start guessing...")
time.sleep(0.5)
word = ("secret")
guesses = ''
t = 10
while t> 0:         
    f = 0                
    for char in word:      
        if char in guesses:    
            print (char,end="")   

        else:
            print ("_",end="")    
            f+= 1    
    if f== 0:        
        print ("\nYou won")
        break            
    guess = input("\nguess a character:") 
    guesses += guess
    if guess not in word:  
        t-= 1        
        print ("Wrong")  
        print ("You have", + turns, 'more guesses' )
    if t== 0:           
        print ("You Lose"  )
