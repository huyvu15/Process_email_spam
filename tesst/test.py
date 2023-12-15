import tkinter as tk
from PIL import Image, ImageTk  # Make sure to import Image module from PIL

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hình Nền Tkinter")
        self.create_gui()
        self.root.mainloop()

    def create_gui(self):
        # Đường dẫn đến ảnh bạn muốn sử dụng làm nền
        background_image_path = "Image/61.jpg"

        # Tạo đối tượng PhotoImage từ ảnh
        background_image = Image.open(background_image_path)
        background_photo = ImageTk.PhotoImage(background_image)

        # Tạo một Label để chứa hình ảnh và đặt nó làm hình nền cho cửa sổ chính
        background_label = tk.Label(self.root, image=background_photo)
        background_label.place(relwidth=1, relheight=1)

        # Thêm các thành phần khác vào cửa sổ hoặc thực hiện các thao tác khác tùy thuộc vào ứng dụng của bạn

if __name__ == "__main__":
    app = App()
