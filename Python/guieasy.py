# Giorgio Valdman - GUI Simple Window

# GUI - Graphic User Interface

from tkinter import *

# Main
window=Tk()

# Title on the windows
window.title("IDIOT")

#Set the windows size
window.geometry("720x1080")

# Change bg color
window.configure(bg="green")

# Create text
writing=Label(window, text="IDIOT",background="red")
writing.pack()

#Run mainloop
window.mainloop
