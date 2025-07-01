# Giorgio Valdman - Hard Challenge

totalcoach=550
# cpp - Coach cost Per Person
cpp=totalcoach/45
singlepark=30
studentcap=45
loop1=1
while loop1>0:
    students =int(input("How many students are taking part in the trip? "))
    if students > studentcap:
        print("Student number is over the limit. ")
    elif students <= studentcap:
        students=students
        loop1=loop1-1
    else :
        print("Unknown Error")
        loop1=loop1-1
# cps - Cost Per Student
totalpark=(30*students)-(students/10)
cps= (550/students) + totalpark
print("The total Cost Per Student is: ",cps)

payed="Payed: "
topay="To Pay: "
student1=input("Student name: ")
student1payment=input("Did they pay? ")
if student1payment=="y":
    payed=payed+student1
elif student1payment=="n":
    topay=topay+student1
student2=input("Student name: ")
student2payment=input("Did they pay? ")
if student2payment=="y":
    payed=payed+student2
elif student2payment=="n":
    topay=topay+student2
student3=input("Student name: ")
student3payment=input("Did they pay? ")
student4=input("Student name: ")
student4payment=input("Did they pay? ")
student5=input("Student name: ")
student5payment=input("Did they pay? ")
student6=input("Student name: ")
student6payment=input("Did they pay? ")
student7=input("Student name: ")
student7payment=input("Did they pay? ")

    

print(payed)
print(topay)

    


