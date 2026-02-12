import tkinter as mrmay

root = mrmay.Tk()
root.title("Grade Check")
root.geometry("600x300")

def grades():
    user_input = float(entry.get())  # Convert input to number
        
    if user_input > 50:
        result = "Passed"
    else:
        result = "Failed"   


    if user_input >= 73:
        grade=7
    elif user_input >= 64 and user_input <= 72:
        grade=6
    elif user_input >= 55 and user_input < 64:
        grade=5
    elif user_input >= 45 and user_input <= 54:
        grade=4

    result = f"You: {result}"
    output_label.config(text=result, fg="green" if result == "Passed" else "red")
    grade = f"Your DP grade: {grade}"
    output_label2.config(text=grade, fg="green" if result == "Passed" else "red")



entry = mrmay.Entry(root, width=30, justify="center")
entry.pack(pady=20)

submit_button = mrmay.Button(root, text="Submit", command=grades)
submit_button.pack(pady=5)

output_label = mrmay.Label(root, text="")
output_label.pack(pady=10)

output_label2 = mrmay.Label(root, text="")
output_label2.pack(pady=10)

root.mainloop()
