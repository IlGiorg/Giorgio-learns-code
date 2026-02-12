grade=int(input("Enter your grade: "))
if grade >= 50:
    print("You passed!")
    if grade >= 73:
        print("DP Grade 7")
    elif grade >= 64 and grade <= 72:
        print("You got a 6!")
    elif grade >= 55 and grade < 64:
        print("You got a 5!")
    elif grade >= 45 and grade<=54:
        print("You got a 4!")
else:
    print("You failed.")
    if grade >= 32 and grade <45:
        print("DP Grade 3")
    elif grade >= 15 and grade < 32:
        print("You got a 2!")
    elif grade >= 0 and grade <= 15:
        print("You got a 1!")