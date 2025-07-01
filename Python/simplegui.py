# Giorgio Valdman - Simple Gui Solution

from tkinter import *

window = Tk()
window.title("Very Cool Program")
window.geometry("1710x1112")
window.configure(bg="#178013")
writing = label = Label(window, text="Hello, World!", bg="red", fg="white")
writing.pack()
window.mainloop()