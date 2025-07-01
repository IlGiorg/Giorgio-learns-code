# Giorgio Valdman - Challenge 8
loop=1
while loop == 1:
    mark= int(input("Please input your mark: "))
    if mark > 75 and mark < 101:
        print("Your mark is A")
    elif mark <75 and mark>60 or mark==60:
        print("B")
    elif mark >= 35 and mark < 60:
        print("C")
    elif mark < 35:
        print("D")
    elif mark > 100:
        print("Please enter a valid value")
    else : print("Error")
