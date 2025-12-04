import time
temps=[30,4,6,89,7,9,10,30,32,25,26,26,27,99,11,47]
openw=28
closew=20
windowstate=0
# 0 is closed, 1 is open
check=0
while True:
    if check>=14:
        check=0
    elif windowstate==0:
        if temps[check] >= openw:
            print("It's over 28 Degrees!",temps[check],"I opened the window for you!")
            check=+1
            windowstate=1
        elif temps[check] <= closew:
            print("The window is already closed.")
            check=+1
            windowstate=1
    elif windowstate==1:
        if temps[check] <= closew:
            print("It's getting quite cold innit! I closed the window for you!")
            check=+1
            windowstate=0
        elif temps[check] >= openw:
            print("The window is already open.")
            check=+1
            windowstate=1
    time.sleep(1)
    