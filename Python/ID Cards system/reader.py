import tkinter as tk
from tkinter import messagebox
from cards import cards_data

def reader():
    print("Reader Type:")
    print("1. Transit")
    print("2. Bike Station")
    choice = input("Enter choice: ").strip()

    if choice not in ["1", "2"]:
        print("Invalid reader type.")
        return

    reader_type = "transit" if choice == "1" else "bike"
    zone = None

    if reader_type == "transit":
        zone = input("Enter station zone (1–9): ").strip()
        if not zone.isdigit() or not (1 <= int(zone) <= 9):
            print("Invalid zone. Must be a number between 1 and 9.")
            return

    window = tk.Tk()
    window.title(f"Card Reader - {reader_type.capitalize()}")
    window.geometry("400x250")

    def check_card():
        card_number = card_entry.get().strip()

        if card_number == "0000":
            window.destroy()
            return

        if not card_number.isdigit():
            messagebox.showerror("Error", "Card number must be digits only.")
            card_entry.delete(0, tk.END)
            return

        card = cards_data.get(card_number)
        if not card:
            messagebox.showerror("Error", "Card not found.")
            card_entry.delete(0, tk.END)
            return

        valid = card.get("valid")
        if valid == "0":
            messagebox.showwarning("Not Valid", "Card is not valid.")
        elif valid == "2":
            messagebox.showwarning("Expired", "Card is expired.")
        elif valid == "3":
            messagebox.showerror("Blacklisted", "Card is blacklisted.")
        elif valid == "8":
            window.destroy()
            return
        else:
            if reader_type == "transit":
                card_zone = card.get("zones", "0")
                if not card_zone.isdigit():
                    messagebox.showerror("Error", "Invalid zone on card.")
                elif int(card_zone) < int(zone):
                    messagebox.showerror("Out of Bounds", f"Card zone ({card_zone}) is lower than station zone ({zone})")
                else:
                    messagebox.showinfo("Access Granted", "Transit access granted!")
            elif reader_type == "bike":
                if card.get("bike", "0") == "1":
                    messagebox.showinfo("Access Granted", "Bike access granted!")
                else:
                    messagebox.showerror("Access Denied", "Card not valid for bike access.")

        card_entry.delete(0, tk.END)  # Clear input after check

    tk.Label(window, text="Enter Card Number:", font=("Arial", 12)).pack(pady=10)
    card_entry = tk.Entry(window, font=("Arial", 12), width=25)
    card_entry.pack()
    card_entry.bind("<Return>", lambda event: check_card())

    tk.Button(window, text="Check Card", command=check_card, font=("Arial", 12), width=20).pack(pady=20)

    window.mainloop()
