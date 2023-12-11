import tkinter as tk
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *

root = tk.Tk()

# Mặc định, bạn có thể sử dụng logo của chính cửa sổ Tkinter
root.title('Ứng dụng với Logo')

icon = PhotoImage(file="Image\client.png")
root.iconphoto(False, icon)

# # Nút để thay đổi logo
# change_logo_button = tk.Button(root, text='Thay Đổi Logo', command=change_logo)
# change_logo_button.pack(pady=20)

# Chạy ứng dụng
root.mainloop()
