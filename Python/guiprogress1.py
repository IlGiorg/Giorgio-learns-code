# Giorgio Valdman - GUI Simple Window

# GUI - Graphic User Interface

from tkinter import *
from tkinter import ttk
import random
def enter(event):
        click()
def click():

    # Main
    window=Tk()

    # Title on the windows
    window.title("IDIOT")

    #Set the windows size
    window.geometry("400x150")

    # Change bg color
    window.configure(bg="green")

    # Create text
    writing=Label(window, text="IDIOT",background="red")
    writing.pack(pady=(20))
    button=ttk.Button(window, text="Quit Program", command=click)
    window.bind_all("<Key>",enter)
    button.pack()
    #Run mainloop
    window.mainloop
click()
