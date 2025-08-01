print("Starting... ")
import startchecks
import status
import shared

print("\nBooting Chairlift...\n")
print("Checking status...\n")


print("Verifying Modules...\n")
print("Gates: "+startchecks.gatestatus)
print("Stop: "+startchecks.stopstatus)
print("Speed: "+startchecks.speedstatus)
print("Errors: "+startchecks.errorsstatus)
print("Reset: "+startchecks.resetstatus)
print("\n")
shared.go=1
status.mainstatus=2


while shared.go==1:
    ask=input("Select Operation: ")
    shared.op=ask
    print(status.readstatus)
