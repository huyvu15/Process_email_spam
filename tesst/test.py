import tkinter as tk
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *

root = tk.Tk()

root.title('Ứng dụng với Logo')

icon = PhotoImage(file="Image\client.png")
root.iconphoto(False, icon)

root.mainloop()
