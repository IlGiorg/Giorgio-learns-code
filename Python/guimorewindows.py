import tkinter as tk

win1=tk.Tk
win2=tk.Tk
win3=tk.Tk

def open_new_window(title, message):
    new_win= tk.Toplevel()
    new_win.title(title)
    new_win.geometry("300x300")
    win1.configure(bg="green")
    
def open_new_window1(title, message):
    new_win= tk.Toplevel()
    new_win.title(title)
    new_win.geometry("300x300")
    win2.configure(bg="light_blue")
    
    
def open_new_window11(title, message):
    new_win= tk.Toplevel()
    new_win.title(title)
    new_win.geometry("300x300")
    win3.configure(bg="navy")

root=tk.Tk()
root.title("Boring GUI")
root.geometry("300x300")


button1= tk.Button(root,  text="Open Windows", command=lambda: open_new_window("Window 1", "This is the first window")) 
button1.pack(pady=5)

button2= tk.Button(root,  text="Open Windows", command=lambda: open_new_window1("Window 2", "This is the second window")) 
button2.pack(pady=5)

button3= tk.Button(root, text="Open Windows", command=lambda: open_new_window11("Window 3", "This is the third window")) 
button3.pack(pady=5)


root.mainloop()
win1.mainloop()
win2.mainloop()
win3.mainloop()
