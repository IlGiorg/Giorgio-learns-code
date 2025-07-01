# Giorgio Valdman - St. Louis vs ICS Milan

print("Welcome to")
print("ICS Milan vs St. Louis")
print("S for St. Louis")
print("I for ICS Milan")
print("X to end the game")
stl=int(0)
ics=int(0)
stop=int(0)
while stop==0:
    team= input("Select team: ")
    if team == "s":
        stll= int(input("How many points? "))
        if stll>3 :
            print("Please enter a valid value")
        stl = stl+stll
        print("ICS: " , ics)
        print("St. Louis: ", stl)

    elif team == "i":
        icss= int(input("How many points? "))
        if icss>3:
            print("Nuh uh")
        else:
            ics=ics+icss
        print("ICS: ", ics)
        print("St. Louis: ", stl)
    elif team == "x":
        stop=stop+1
        print("St. Louis: ",stl)
        print("ICS Milan: ", ics)
        if stl>ics:
            print("St. Louis Wins!")
        elif ics>stl:
            print("ICS Milan Wins!")
        elif ics == stl:
            print("It's a tie!")
        else: print("Error")
    else : print("Error")