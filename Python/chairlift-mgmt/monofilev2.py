from pygame import *
import random
print("Starting... ")

print("\nBooting Chairlift...\n")
print("Checking status...\n")


print("Verifying Modules...\n")
print("No Modules Found!")
mainstatus=0
statuscheck=1
readstatus="System just booted. Not Ready."
go=0
startcodes=(808081, 909187, 676754, 515158, 494941)
setgocode=random.choice(startcodes)
setgo=int(input("Please input "+ str(setgocode) + " to set system as ready  "))

if setgo==setgocode:
    go=1
    print("System is now starting")
    print(readstatus)
else: print("Error. Quitting program...")

# 0: Default
# 1: Running
# 2: Ready
# 3: Emergency Stop
# 4: Service Stop
# 5: Slowed 1
# 6: Slowed 2
# 7: Awating Reset
# 8:
# 9: ERROR

dir=1
reset=0
speed=100
while go==1:
    print("\n\n")
    
    op=input("\nSelect Operation: ")
    #start
    # e - Emergency Stop
    # ss - Service Stop
    # s1 - Slow Level 1
    # s2 - Slow Level 2
    # rr - Reset
    # invert - Switch direction
    # quitquit - Quit Program
    # dict - Show Dictionary of Operations

    if op=="start":
        if mainstatus==2:
            if reset==1:
                mainstatus=1
        elif mainstatus==5:
            speed=100
            mainstatus=1
        elif mainstatus==6:
            speed=100
            mainstatus=1
        elif mainstatus==1:
            print("")
        elif mainstatus==9:
            print("There's an error open. Enter errxrs to solve.")
        else: print("Something Went Wrong :/")
        if reset==0:
            mainstatus=7
            print("\nSystem is not ready")
    elif op=="dict":
        print("\n\n")
        print("start - Start the lift")
        print("e - Emergency Stop")
        print("nn e - Lift will be ready to start, but won't start until start is entered")
        print("ss - Service Stop")
        print("s1 - Slow Level 1")
        print("s2 - Slow Level 2")
        print("rr - Reset")
        print("invert - Switch direction")
        print("quitquit - Quit Program\n\n")
    elif op=="e":
        mainstatus=3
        reset=0
    elif op=="nn e":
        mainstatus=7
    elif op=="ss":
        mainstatus=4
        reset=0
    elif op=="s1":
        mainstatus=5
        speed=75
        print("Speed was slowed down to: 75%")
    elif op=="s2":
        mainstatus=6
        speed=50
        print("Speed was slowed down to: 50%")
    elif op=="rr":
        if mainstatus != 3:
            if mainstatus==4:
                liftss=input("Are you sure you want to lift Service Stop? 50505x  ")
                if liftss=="50505x":
                    mainstatus=2
                    reset=1
            else: 
                mainstatus=2
                reset=1
    elif op=="invert":
        if mainstatus==2:
            invertcheck=input("Are you sure you want to invert direction of travel? 1/0 ")
            if invertcheck=="1":
                if dir==2:
                    dir=1
                    print("Direction of travel is now: Forward")
                elif dir==1:
                    dir=2
                    print("Direction of travel is now: Backwards")
            elif invertcheck==0:
                print("Quitting invert function...\n")
        elif mainstatus==1:
            print("Can't complete operation: Lift is running.\n The lift will now stop with stopcode: 9xdir\nTo reset, enter: errxrs")
            mainstatus=9
    elif op=="errxrs":
        print("Please make sure the error has been solved before resetting.\nThe system won't start if it will and a general systems restart will be necessary.")
        errreset=input("Do you understand? 1 ")
        if errreset=="1":
            mainstatus=2
        else: 
            print("Crytical System Error. System shutting down...")
            go=0
            break
    elif op=="quitquit":
        surequit=input("Are you sure you want to exit? y/n")
        if surequit=="y":
             print("Stopping Chairlift...")
             print("Exiting Software...")
             print("Closing Operations...")
             print("\nGoodbye!")
             break
        elif surequit=="n":
            print("Canceled")
    
    if mainstatus==0:
        readstatus="Default - Booting"
    elif mainstatus==1:
        readstatus="Running"
    elif mainstatus==2:
        readstatus="Ready"
    elif mainstatus==3:
        readstatus="Emergency Stop"
    elif mainstatus==4:
        readstatus="Service Stop"
    elif mainstatus==5:
        readstatus="Slowed 1"
    elif mainstatus==6:
        readstatus="Slowed 2"
    elif mainstatus==7:
        readstatus="Awaiting Reset"
    elif mainstatus==9:
        readstatus="Error"
    print(readstatus)

    # e - Emergency Stop
    # ss - Service Stop
    # s1 - Slow Level 1
    # s2 - Slow Level 2
    # invert - Switch direction
    # quitquit - 