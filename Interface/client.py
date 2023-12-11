import socket
import tkinter as tk
from tkinter import ttk, scrolledtext

class GmailClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gmail Client")
        self.root.geometry("600x400")

        self.create_gui()

    def create_gui(self):
        # Compose Frame
        compose_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        compose_frame.grid(row=0, column=0, sticky="nsew")

        # To Label
        to_label = ttk.Label(compose_frame, text="To:")
        to_label.grid(row=0, column=0, pady=5, sticky="w")

        to_entry = ttk.Entry(compose_frame, width=50)
        to_entry.grid(row=0, column=1, pady=5, sticky="w")

        # Subject Label
        subject_label = ttk.Label(compose_frame, text="Subject:")
        subject_label.grid(row=1, column=0, pady=5, sticky="w")

        subject_entry = ttk.Entry(compose_frame, width=50)
        subject_entry.grid(row=1, column=1, pady=5, sticky="w")

        # Body Label
        body_label = ttk.Label(compose_frame, text="Body:")
        body_label.grid(row=2, column=0, pady=5, sticky="w")

        body_text = scrolledtext.ScrolledText(compose_frame, wrap=tk.WORD, width=70, height=5)
        body_text.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        # Send Button
        send_button = ttk.Button(compose_frame, text="Send", command=lambda: self.send_message(to_entry.get(), subject_entry.get(), body_text.get(1.0, tk.END)))
        send_button.grid(row=3, column=1, pady=10, sticky="e")

        # Received Messages
        received_label = ttk.Label(compose_frame, text="Received Messages", font=("Helvetica", 12, "bold"))
        received_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        self.received_text = scrolledtext.ScrolledText(compose_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 12))
        self.received_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        compose_frame.columnconfigure(1, weight=1)
        compose_frame.rowconfigure(5, weight=1)

    def send_message(self, to, subject, body):
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
