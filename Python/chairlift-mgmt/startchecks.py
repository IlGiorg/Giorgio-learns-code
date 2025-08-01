import gates
import speed
import stop
import errors
import reset

if gates.gatescheck==1:
    gatestatus="Imported Successfully"
else: 
    gatestatus="Error"
if speed.speedcheck==1:
    speedstatus="Imported Successfully"
else: 
    speedastatus="Error"

if stop.stopcheck==1:
    stopstatus="Imported Successfully"
else: 
    stopstatus="Error"
if errors.errorscheck==1:
    errorsstatus="Imported Successfully"
else: 
    errorsstatus="Error"
if reset.resetcheck==1:
    resetstatus="Imported Successfully"
else: 
    resetstatus="Error"
