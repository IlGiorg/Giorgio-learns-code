# Giorgio Valdman - Computer Science - Rock Paper Scissors Challenge 10

# import the module used in python to get random values
import random

# asks the user input with the variable "user" and makes it convert to lowercase
user = input("Enter rock, paper, or scissors: ").lower()

# specifies that the option must be amongst the three words defined in the dictionary
if user not in ['rock', 'paper', 'scissors']:
    print("Invalid choice! Please run the program again.")


else:
    # computer choice using random.choice thanks to the previously imported module
    computer = random.choice(['rock', 'paper', 'scissors'])
    
    # Prints the choices 
    print(f"\nComputer chose:",computer)
    print(f"You chose:",user)
    
    # Different cases to print and decide who won
    if user == computer:
        print("It's a tie!")
    elif (user == 'rock' and computer == 'scissors') or \
         (user == 'paper' and computer == 'rock') or \
         (user == 'scissors' and computer == 'paper'):
        print("You win!")
    else:
        print("Computer wins!")


















#
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
##
#
#
#
#
#








# Commented by Giorgio Valdman