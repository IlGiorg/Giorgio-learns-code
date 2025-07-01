import tkinter as tk

window = tk.Tk()
window.title("Greetings,          all.")
window.geometry("1710x1112")
window.configure(bg="#178013")

label = tk.Label(window, text="Enter your name: ", font=("Arial", 50))
label.pack()

# Text Entry Box
entry = tk.Entry(window, font=("Arial", 50))
entry.pack()

def say_hello():
    name = entry.get()
    greeting = f"Hello, {name}!"
    result_label.config(text=greeting)

button = tk.Button(window, text="Greet me", command=say_hello, font=("Arial", 50))
button.pack()

result_label = tk.Label(window, text="", font=("Arial", 50))
result_label.pack()

window.mainloop()
