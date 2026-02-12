import tkinter as mrmay

root = mrmay.Tk()
root.title("Grade Check")
root.geometry("600x300")

def grades():
    try:
        user_input = float(entry.get())  # Convert input to number
        
        if user_input > 50:
            grade = "Passed"
        else:
            grade = "Failed"
            
        result = f"You: {grade}"
        output_label.config(text=result, fg="green" if grade == "Passed" else "red")
    
    except ValueError:
        output_label.config(text="Please enter a valid number", fg="orange")

entry = mrmay.Entry(root, width=30, justify="center")
entry.pack(pady=20)

submit_button = mrmay.Button(root, text="Submit", command=grades)
submit_button.pack(pady=5)

output_label = mrmay.Label(root, text="")
output_label.pack(pady=10)

root.mainloop()
