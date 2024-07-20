# Import Module
from tkinter import *
from PIL import Image, ImageTk

# create root window
root = Tk()

# root window title and dimension
root.title("Welcome to !CultChat")
# Set geometry (widthxheight)

root.eval('tk::PlaceWindow . center')
width = int(root.winfo_screenwidth() * .5)
height = int(root.winfo_screenheight() * .5)
x = (root.winfo_screenwidth() - width)//2
# y = root.winfo_screenheight() - height

root.geometry(f"{width}x{height}+{x}+{0}")


image = Image.open("output.jpg")
image = ImageTk.PhotoImage(image)

# image = root.Label()

lbl = Label(root, image=image)

lbl.grid()

# root.geometry('350x200')

# all widgets will be here
# Execute Tkinter
root.mainloop()
