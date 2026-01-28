

OldList=["welcome2021", "letmein!", "qwerty", "abc123","XXXX"]
NewPassword=input("Enter your new password: ")
posn=1
found=False
while found==False and OldList[posn]!="XXXX":
    if NewPassword==OldList[posn]:
        found=True
    else:
        posn=posn+1
        found=False
if found==True:
    print("Password rejected. Choose a different password.")
else:
    print("Password accepted.")