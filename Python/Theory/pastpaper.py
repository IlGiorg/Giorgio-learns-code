quote="Learning Never Exhausts The Mind"
Start=24
Number=8
substring=quote[Start:Start+Number]
print(substring)
print(quote.lower())

##############

toohot=0
toocold=0
loop=True
while loop==True:
    temp=int(input("Enter temperature "))
    if temp < -25:
        toocold= toocold+1
    elif temp > -18:
        toohot= toohot=+1
    if toohot > 5 or toocold > 10:
        loop==False

if toohot > 5:
    print("Alarm!!")

if toocold > 10:
    print("Call The engineer")