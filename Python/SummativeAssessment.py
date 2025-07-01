# Giorgio Valdman - Summative Assessment - Clear Windows

loop=True

# CONSTANTS - Constants never change and should be written always in uppercase
BASIC_CLEAN=10.00
ADDITIONAL_WIN=5.00
SOLAR_PANELS=20.00

while loop==True:
    # Variables
    # We create 11 empty variable
    # Customer ID, Name, Address, Service 1, Service 2, Service 3, Service 4, Service 5, Service 6, Service 7, Total

    customer_details=[0]*11
    customer_id=0

    # Price Changes

    print("Welcome to Clear Windows")
    print("")
    print("1: Basic Window clean, outside, only one floor, up to five windows                          $10.00")
    print("2: Additional windows up to and including 5                                                  $5.00")
    print("3: Two floors                                                                            10% extra")
    print("4: Three floors                                                                          15% extra")
    print("5: Inside as well                                                                        25% extra")
    print("6: Polish all windows                                                                     5% extra")
    print("7: Special Solar panel cleaning                                                             $20.00\n")

    customer_details[0]=customer_id+1
    customer_id=customer_id+1
    customer_details[1]=input("What is your name? ")
    customer_details[2]=input("What is your address? ")

    service1=str(input("Do you want service 1? Y/N ")).lower()
    if service1=="y":
        customer_details[3]=BASIC_CLEAN
        service2=str(input("Do you want service 2? y/n ")).lower()
        if service2=="y":
            customer_details[4]=ADDITIONAL_WIN
            service34=int(input("Do you want service 3 or service 4? "))
            if service34==3:
                customer_details[5]=(customer_details[3]+customer_details[4])*0.1
                customer_details[6]=0
            elif service34==4:
                    customer_details[6]=(customer_details[3]+customer_details[4])*0.15
                    customer_details[5]=0
            else:print("Error: Value not valid")
            service5=str(input("Do you want service 5? ")).lower()
            if service5=="y":
                customer_details[7]=round((customer_details[3]+customer_details[4]+customer_details[5]+customer_details[6])*0.25,2)
                service6 = str(input("Do you want service 6? ")).lower()
            else:print("Error: Value not valid")
            if service6 == "y":
                customer_details[8] = round((customer_details[3] + customer_details[4] + customer_details[5] +customer_details[6]+customer_details[7]) * 0.05,2)
                service7 = str(input("Do you want service 7? ")).lower()
            else:print("Error: Value not valid")
            if service7 == "y":
                    customer_details[9] = SOLAR_PANELS
            else:print("Error: Value not valid")
        else:print("Error: Value not valid")
        
        invoice=str(customer_details)
        f=open("Cleaning.txt","a")
        f.write(invoice)
        f.write("\n")
        f.close()


    elif service1=="n":
        customer_details[3]=0
        service7=str(input("Do you want service 7? ")).lower
        if service7=="y":
            customer_details[9] = SOLAR_PANELS
        elif service7=="n":
            customer_details[9]=0
        else:print("Error: Value not valid")
    else : print("Error: Value not valid")
    customer_details[10]=customer_details[3]+customer_details[4]+customer_details[5]+customer_details[6]+customer_details[7]+customer_details[8]+customer_details[9]
    print("")
    print("INVOICE\n")
    print("Customer ID: ",customer_details[0])
    print("Name: ",customer_details[1])
    print("Address: ",customer_details[2])
    print("Basic Window Clean: ",customer_details[3])
    print("Additional Windows: ",customer_details[4])
    print("Two Floors: ",customer_details[5])
    print("Three Floors: ",customer_details[6])
    print("Inside as Well: ",customer_details[7])
    print("Polish all windows: ",customer_details[8])
    print("Spacial Solar Panel Cleaning: ",customer_details[9])
    print("Total: ",customer_details[10])
    print("")
    print("-----------------------------------")
    print("\n\n")
