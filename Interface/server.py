import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import socket
import threading

class GmailServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gmail Server")
        self.root.geometry("800x600")

        self.messages = []
        self.clients = []
        self.message_index = 1

        self.create_gui()

        threading.Thread(target=self.start_server).start()

    def create_gui(self):
        # Header Frame
        header_frame = ttk.Frame(self.root, padding=(10, 10, 10, 0))
        header_frame.grid(row=0, column=0, sticky="ew")

        # Inbox Frame
        inbox_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        inbox_frame.grid(row=1, column=0, sticky="nsew")

        # Email Frame
        email_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        email_frame.grid(row=2, column=0, sticky="nsew")

        # Header
        ttk.Label(header_frame, text="Gmail", font=("Helvetica", 16, "bold")).grid(row=0, column=0)

        # Inbox
        inbox_label = ttk.Label(inbox_frame, text="Inbox", font=("Helvetica", 14, "bold"))
        inbox_label.grid(row=0, column=0, sticky="w")

        self.listbox = tk.Listbox(inbox_frame, selectmode=tk.SINGLE, width=50, height=15, font=("Helvetica", 12))
        self.listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.listbox.bind('<<ListboxSelect>>', self.display_selected_message)

        delete_button = ttk.Button(inbox_frame, text="Delete", command=self.delete_selected_message)
        delete_button.grid(row=2, column=0, pady=10, sticky="w")

        # Email Display
        email_display_label = ttk.Label(email_frame, text="Email", font=("Helvetica", 14, "bold"))
        email_display_label.grid(row=0, column=0, sticky="w")

        self.email_display_text = scrolledtext.ScrolledText(email_frame, wrap=tk.WORD, width=70, height=10, font=("Helvetica", 12))
        self.email_display_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

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
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                timestamp = datetime.now().strftime("%H:%M:%S")
                message = f"{self.message_index}. {timestamp} - Client: {data.decode('utf-8')}\n"
                self.messages.append(message)
                self.listbox.insert(tk.END, f"{self.message_index}. Client - {timestamp}")
                self.message_index += 1
                self.root.update_idletasks()
            except ConnectionResetError:
                break

    def display_selected_message(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            selected_message = self.messages[selected_index]
            self.email_display_text.delete(1.0, tk.END)
            self.email_display_text.insert(tk.END, selected_message)

    def delete_selected_message(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            self.listbox.delete(selected_index)
            del self.messages[selected_index]

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gmail_server = GmailServer()
    gmail_server.run()
