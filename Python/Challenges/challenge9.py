# Giorgio Valdman - Challenge 9
loop = 1
while loop > 0:
    value = input("Enter one of the Olympics values: ").lower()
    
    if value == "respect":
        print("Good job!")
        again = input("Do you want to play again? Y or N ").lower()
        if again == "y":
            print("Loading...")
        elif again == "n":
            print("Goodbye!")
            loop = loop - 1

    elif value == "excellence":
        print("Good job!")
        again = input("Do you want to play again? Y or N ").lower()
        if again == "y":
            print("Loading...")
        elif again == "n":
            print("Goodbye!")
            loop = loop - 1

    elif value == "friendship":
        print("Good job!")
        again = input("Do you want to play again? Y or N ").lower()
        if again == "y":
            print("Loading...")
        elif again == "n":
            print("Goodbye!")
            loop = loop - 1

    else:
        print("Wrong :/")
        again = input("Do you want to play again? Y or N ").lower()
        if again == "y":
            print("Loading...")
        elif again == "n":
            print("Goodbye!")
            loop = loop - 1
