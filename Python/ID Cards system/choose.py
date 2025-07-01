def get_user_choice():
    print("\n--- Main Menu ---")
    print("1. Read Card")
    print("2. Write Card")
    print("3. Create New Card")
    print("4. Card Reader")
    print("5. Logout")
    print("6. Check Expiry Dates")

    while True:
        choice = input("Enter your choice (1–5): ")
        if choice in ["1", "2", "3", "4", "5","6"]:
            return int(choice)
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")
