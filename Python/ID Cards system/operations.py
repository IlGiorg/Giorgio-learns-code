from cards import cards_data
def read_card():
    card_number = input("Enter card number: ").strip()

    if not card_number.isdigit():
        print("Invalid input. Card number must be digits only.")
        return

    if card_number in cards_data:
        print("\n--- Card Information ---")
        for key, value in cards_data[card_number].items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("Card not found.")


def write_card():
    card_number = input("Enter card number to edit: ").strip()

    if not card_number.isdigit():
        print("Invalid input. Card number must be digits only.")
        return

    if card_number not in cards_data:
        print("Card not found.")
        return

    print("\n--- Current Card Info ---")
    for key, value in cards_data[card_number].items():
        print(f"{key.capitalize()}: {value}")

    print("\n--- Edit Fields ---")
    for field in cards_data[card_number]:
        current_value = cards_data[card_number][field]
        new_value = input(f"Enter new value for {field} (leave blank to keep '{current_value}'): ").strip()
        if new_value:
            cards_data[card_number][field] = new_value
            print(f"{field} updated.")

    print("\nCard updated successfully.")
    import json
import ast

def create_new_card():
    card_number = input("Enter new card number: ").strip()

    if not card_number.isdigit():
        print("Card number must be digits only.")
        return

    if card_number in cards_data:
        print("Card already exists.")
        return

    name = input("Enter name: ").strip()
    type_ = input("Enter type (e.g. yearly): ").strip()
    zones = input("Enter zones: ").strip()
    bike = input("Bike access (yes/no): ").strip()
    expires = input("Enter expiry date (YYYY-MM-DD): ").strip()
    valid = input("Valid (1 = Valid, 0 = Not Valid, 2 = Expired, 3 = Blacklisted): ").strip()

    cards_data[card_number] = {
        "name": name,
        "type": type_,
        "zones": zones,
        "bike": bike,
        "expires": expires,
        "valid": valid
    }

    # Save back to cards.py using repr() to preserve Python dict syntax
    try:
        with open("cards.py", "w") as f:
            f.write("cards_data = ")
            f.write(repr(cards_data))
        print("✅ New card created and saved.")
    except Exception as e:
        print(f"❌ Failed to save card: {e}")
from datetime import datetime
from cards import cards_data

def check_and_update_expiry():
    today_input = input("Enter today's date (ddmmyyyy): ").strip()

    if len(today_input) != 8 or not today_input.isdigit():
        print("Invalid date format.")
        return

    try:
        today = datetime.strptime(today_input, "%d%m%Y").date()
    except ValueError:
        print("Invalid date.")
        return

    updated = False

    for card_number, card in cards_data.items():
        expires_str = card.get("expires", "")
        try:
            expires_date = datetime.strptime(expires_str, "%Y-%m-%d").date()
            if expires_date < today and card.get("valid") != "2":
                card["valid"] = "2"
                print(f"Card {card_number} marked as expired.")
                updated = True
        except ValueError:
            print(f"Invalid expiry date format on card {card_number}.")

    if updated:
        try:
            with open("cards.py", "w") as f:
                f.write("cards_data = ")
                f.write(repr(cards_data))
            print("✅ Expired cards updated and saved.")
        except Exception as e:
            print(f"❌ Failed to save updated cards: {e}")
    else:
        print("No cards needed updating.")


