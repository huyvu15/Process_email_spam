import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import socket
import threading
import os
from PIL import Image, ImageTk
import random
# from tkinter import *
# from tkinter.ttk import *
from NaiveBayes import NaiveBayes
import pandas as pd


# if __name__ == "__main__":
def a():
    sms_spam = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])

    # Randomize the dataset
    data_randomized = sms_spam.sample(frac=1, random_state=1)
    # Calculate index for split
    training_test_index = round(len(data_randomized) * 0.8)
    # Split into training and test sets
    training_set = data_randomized[:training_test_index].reset_index(drop=True)

    # Tạo và huấn luyện mô hình
    spam_classifier = NaiveBayes(alpha=1)
    spam_classifier.train(training_set)

    # Sử dụng mô hình để phân loại tin nhắn
    mess = """
    WorldQuant BRAIN Việt Nam hân hạnh được tổ chức buổi gặp gỡ tháng 12/2023 dành riêng cho các bạn BRAIN consultant onboard trong năm 2023!
    """

    result = spam_classifier.classify(mess)
    if result:
        print("Ham")
    else:
        print("Spam")

class GmailServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gmail Server")
        self.root.geometry("800x600")
        
        # icon = PhotoImage(file="Image\Server1.png")
        # self.root.iconphoto(False, icon)

        self.messages = []
        self.clients = []
        self.message_index = 1

        self.create_gui()

        threading.Thread(target=self.start_server).start()

    def create_gui(self):
        # Inbox Frame
        inbox_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        inbox_frame.grid(row=0, column=0, sticky="nsew")

        # Email Frame
        email_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        email_frame.grid(row=1, column=0, sticky="nsew")

        # Inbox
        inbox_label = ttk.Label(inbox_frame, text="Inbox", font=("Helvetica", 16, "bold"))
        inbox_label.grid(row=0, column=0, sticky="w")

        self.listbox = tk.Listbox(inbox_frame, selectmode=tk.SINGLE, width=60, height=10, font=("Helvetica", 12))
        self.listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.listbox.bind('<<ListboxSelect>>', self.display_selected_message)

        delete_button = ttk.Button(inbox_frame, text="Delete", command=self.delete_selected_message)
        delete_button.grid(row=2, column=0, pady=10, sticky="w")

        # Email Display
        email_display_label = ttk.Label(email_frame, text="Email", font=("Helvetica", 16, "bold"))
        email_display_label.grid(row=0, column=0, sticky="w")

        self.email_display_frame = ttk.Frame(email_frame)
        self.email_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.email_display_text = scrolledtext.ScrolledText(self.email_display_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 12))
        self.email_display_text.grid(row=0, column=0, sticky="nsew")

        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        inbox_frame.columnconfigure(0, weight=1)
        inbox_frame.rowconfigure(1, weight=1)

        email_frame.columnconfigure(0, weight=1)
        email_frame.rowconfigure(1, weight=1)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 5555))
        server_socket.listen(5)

        while True:
            client, addr = server_socket.accept()
            self.clients.append(client)
            threading.Thread(target=self.receive_messages, args=(client,)).start()

    def receive_messages(self, client):
        try:
            data = client.recv(1024)
            if not data:
                return
            timestamp = datetime.now().strftime("%H:%M:%S")
            avatar_path = self.get_random_avatar_path()
            avatar_image = self.load_avatar_image(avatar_path)
            message = f"{self.message_index}. {timestamp} - Huy: {data.decode('utf-8')}\n"
            self.messages.append((message, avatar_image))
            self.listbox.insert(tk.END, f"{self.message_index}. Client - {timestamp}")
            self.message_index += 1
            self.root.update_idletasks()
        except ConnectionResetError:
            pass

    def display_selected_message(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            selected_message, selected_avatar = self.messages[selected_index]
            self.display_email(selected_message, selected_avatar)

    def delete_selected_message(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            self.listbox.delete(selected_index)
            del self.messages[selected_index]

    def display_email(self, message, avatar):
        for widget in self.email_display_frame.winfo_children():
            widget.destroy()

        avatar_label = tk.Label(self.email_display_frame, image=avatar, borderwidth=2, relief="solid", width=100, height=100)
        avatar_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        text_widget = scrolledtext.ScrolledText(self.email_display_frame, wrap=tk.WORD, width=60, height=8, font=("Helvetica", 12))
        text_widget.grid(row=0, column=1, sticky="nsew")
        text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)

    def get_random_avatar_path(self):
        avatar_dir = "Image"
        avatar_files = [f for f in os.listdir(avatar_dir) if f.startswith("avatar-") and f.endswith(".png")]
        if avatar_files:
            return os.path.join(avatar_dir, random.choice(avatar_files))
        return ""

    def load_avatar_image(self, path):
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((100, 100), resample=Image.Resampling.LANCZOS)
            # Giữ tham chiếu đến đối tượng PhotoImage
            img_photo = ImageTk.PhotoImage(img)
            return img_photo
        return None

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gmail_server = GmailServer()
    gmail_server.run()
