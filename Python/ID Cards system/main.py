from login import loginfn
from choose import get_user_choice
from operations import read_card
from operations import write_card
from operations import create_new_card
from reader import reader
from operations import check_and_update_expiry

retrylogin=1

print("Welcome to GiorgioID")


while True:
    username = input("Enter username: ")
    password = input("Enter password: ")
    if loginfn(username, password):
        print("Login successful!")

        while True:
            choice = get_user_choice()

            if choice == 1:
                read_card()
            elif choice == 2:
                write_card()
            elif choice == 3:
                create_new_card()
            elif choice == 4:
                reader()
            elif choice == 5:
                print("Logging out...")
                break
            elif choice == 6:
                check_and_update_expiry()
    else:
        print("Invalid login. Access denied.")
