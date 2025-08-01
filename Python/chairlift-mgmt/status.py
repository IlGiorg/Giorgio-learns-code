import shared
statuscheck=1
mainstatus=0
readstatus="000 Default 000"

while shared.go==1:
    if mainstatus==0:
        readstatus="Default - Booting"
    elif mainstatus==1:
        readstatus="Running"
    elif mainstatus==2:
        readstatus="Ready"
    elif mainstatus==3:
        readstatus="Emergency Stop"

# 0: Default
# 1: Running
# 2: Ready
# 3: Emergency Stop
# 4: Service Stop
# 5: Slowed 1
# 6: Slowed 2
# 7:
# 8:
# 9: ERROR