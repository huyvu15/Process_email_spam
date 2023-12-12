import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import socket
import threading
import os
from PIL import Image, ImageTk
import random
import pandas as pd
from NaiveBayes import NaiveBayes  

class GmailServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gmail Server")
        self.root.geometry("800x600")

        self.ham_messages = []
        self.spam_messages = []

        self.message_index = 1  # Thêm dòng này để khởi tạo self.message_index

        self.create_gui()

        threading.Thread(target=self.start_server).start()
        

    def create_gui(self):
        # Inbox Frame
        inbox_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        inbox_frame.grid(row=0, column=0, sticky="nsew")

        # Ham Listbox
        ttk.Label(inbox_frame, text="Ham Inbox", font=("Helvetica", 16, "bold")).grid(row=0, column=0, sticky="w")
        self.ham_listbox = tk.Listbox(inbox_frame, selectmode=tk.SINGLE, width=60, height=10, font=("Helvetica", 12))
        self.ham_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.ham_listbox.bind('<<ListboxSelect>>', self.display_selected_message)

        # Spam Listbox
        ttk.Label(inbox_frame, text="Spam Inbox", font=("Helvetica", 16, "bold")).grid(row=0, column=1, sticky="w")
        self.spam_listbox = tk.Listbox(inbox_frame, selectmode=tk.SINGLE, width=60, height=10, font=("Helvetica", 12))
        self.spam_listbox.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.spam_listbox.bind('<<ListboxSelect>>', self.display_selected_message)

        delete_ham_button = ttk.Button(inbox_frame, text="Delete Ham", command=lambda: self.delete_selected_message('ham'))
        delete_ham_button.grid(row=2, column=0, pady=10, sticky="w")

        delete_spam_button = ttk.Button(inbox_frame, text="Delete Spam", command=lambda: self.delete_selected_message('spam'))
        delete_spam_button.grid(row=2, column=1, pady=10, sticky="w")

        # Email Frame
        email_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        email_frame.grid(row=1, column=0, sticky="nsew")

        # Email Display
        email_display_label = ttk.Label(email_frame, text="Email", font=("Helvetica", 16, "bold"))
        email_display_label.grid(row=0, column=0, sticky="w")

        self.email_display_frame = ttk.Frame(email_frame)
        self.email_display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.email_display_text = scrolledtext.ScrolledText(self.email_display_frame, wrap=tk.WORD, width=60, height=8, font=("Helvetica", 12))
        self.email_display_text.grid(row=0, column=0, sticky="nsew")

        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        inbox_frame.columnconfigure(0, weight=1)
        inbox_frame.columnconfigure(1, weight=1)
        inbox_frame.rowconfigure(1, weight=1)

        email_frame.columnconfigure(0, weight=1)
        email_frame.rowconfigure(1, weight=1)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 5555))
        server_socket.listen(5)

        while True:
            client, addr = server_socket.accept()
            threading.Thread(target=self.receive_messages, args=(client,)).start()

    def receive_messages(self, client):
        try:
            data = client.recv(1024)
            if not data:
                return
            timestamp = datetime.now().strftime("%H:%M:%S")
            avatar_path = self.get_random_avatar_path()
            avatar_image = self.load_avatar_image(avatar_path)
            message_content = data.decode('utf-8')

            # Phân loại tin nhắn thành Ham hoặc Spam
            result = spam_classifier.classify(message_content)
            if result == False:
                # Phân loại là Spam3
                print(f"Predicted: Spam - Actual: {message_content}")
                message = f"{self.message_index}. {timestamp} - Client (Spam): {message_content}\n"
                self.spam_messages.append((message, avatar_image))
                self.spam_listbox.insert(tk.END, f"{self.message_index}. Client - {timestamp}")
            else:
                print(f"Predicted: Ham - Actual: {message_content}")
                message = f"{self.message_index}. {timestamp} - Client (Ham): {message_content}\n"
                self.ham_messages.append((message, avatar_image))
                self.ham_listbox.insert(tk.END, f"{self.message_index}. Client - {timestamp}")

            self.message_index += 1
            self.root.update_idletasks()
        except ConnectionResetError:
            pass


    def display_selected_message(self, event):
        selected_ham_index = self.ham_listbox.curselection()
        selected_spam_index = self.spam_listbox.curselection()

        if selected_ham_index:
            selected_index = int(selected_ham_index[0])
            selected_message, selected_avatar = self.ham_messages[selected_index]
        elif selected_spam_index:
            selected_index = int(selected_spam_index[0])
            selected_message, selected_avatar = self.spam_messages[selected_index]
        else:
            return

        self.display_email(selected_message, selected_avatar)

    def delete_selected_message(self, inbox_type):
        selected_ham_index = self.ham_listbox.curselection()
        selected_spam_index = self.spam_listbox.curselection()

        if inbox_type == 'ham' and selected_ham_index:
            selected_index = int(selected_ham_index[0])
            self.ham_listbox.delete(selected_index)
            del self.ham_messages[selected_index]
        elif inbox_type == 'spam' and selected_spam_index:
            selected_index = int(selected_spam_index[0])
            self.spam_listbox.delete(selected_index)
            del self.spam_messages[selected_index]

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
            img_photo = ImageTk.PhotoImage(img)
            return img_photo
        return None

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    sms_spam = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])
    data_randomized = sms_spam.sample(frac=1, random_state=1)
    training_test_index = round(len(data_randomized) * 0.8)
    training_set = data_randomized[:training_test_index].reset_index(drop=True)

    spam_classifier = NaiveBayes(alpha=1)
    spam_classifier.train(training_set)

    gmail_server = GmailServer()
    gmail_server.run()