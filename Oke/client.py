import socket
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *

class GmailClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gmail Client")
        self.root.geometry("600x400")

        icon = PhotoImage(file="Image\client.png")
        self.root.iconphoto(False, icon)
        
        self.create_gui()

    def create_gui(self):
        # Compose Frame
        compose_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        compose_frame.grid(row=0, column=0, sticky="nsew")

        # To
        ttk.Label(compose_frame, text="To:").grid(row=0, column=0, sticky="w")
        to_choices = ["Jennie", "Roses", "Jisoo", "Lisa"]
        self.to_combobox = ttk.Combobox(compose_frame, values=to_choices, state="readonly", width=20)
        self.to_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Subject
        ttk.Label(compose_frame, text="Subject:").grid(row=1, column=0, sticky="w")
        subject_choices = ["Em ăn cơm chưa.", "I don't know.", "Chào e, anh đứng đây từ nãy.", "Cho a làm quen nhé"]
        self.subject_combobox = ttk.Combobox(compose_frame, values=subject_choices, state="readonly", width=20)
        self.subject_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Body
        ttk.Label(compose_frame, text="Message Body:").grid(row=2, column=0, sticky="w")
        self.body_text = scrolledtext.ScrolledText(compose_frame, wrap=tk.WORD, width=50, height=10, font=("Helvetica", 12))
        self.body_text.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Send Button
        send_button = ttk.Button(compose_frame, text="Send", command=self.send_message)
        send_button.grid(row=3, column=0, pady=10, sticky="w")

        # Received Messages Frame
        received_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        received_frame.grid(row=1, column=0, sticky="nsew")

        # Received Messages
        ttk.Label(received_frame, text="Received Messages:").grid(row=0, column=0, sticky="w")
        self.received_text = scrolledtext.ScrolledText(received_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 12))
        self.received_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        compose_frame.columnconfigure(1, weight=1)
        compose_frame.rowconfigure(2, weight=1)

        received_frame.columnconfigure(0, weight=1)
        received_frame.rowconfigure(1, weight=1)

    def send_message(self):
        to = self.to_combobox.get()
        subject = self.subject_combobox.get()
        body = self.body_text.get("1.0", tk.END)

        if to and subject and body:
            message = f"To: {to}\nSubject: {subject}\n{body}"
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 5555))
            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()

            # Update received messages in the client UI
            self.received_text.insert(tk.END, f"Sent to: {to}\nSubject: {subject}\n{body}\n\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gmail_client = GmailClient()
    gmail_client.run()
