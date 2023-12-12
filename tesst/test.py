import tkinter as tk
from tkinter import ttk, scrolledtext
from NaiveBayes import NaiveBayes
import pandas as pd

class GmailClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gmail Client")
        self.root.geometry("800x600")

        self.ham_messages = []
        self.spam_messages = []

        self.create_gui()

    def create_gui(self):
        inbox_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        inbox_frame.grid(row=0, column=0, sticky="nsew")

        ham_frame = ttk.Frame(inbox_frame, padding=(10, 10, 10, 10))
        ham_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        spam_frame = ttk.Frame(inbox_frame, padding=(10, 10, 10, 10))
        spam_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(ham_frame, text="Ham Messages").grid(row=0, column=0, sticky="w")
        self.ham_listbox = tk.Listbox(ham_frame, selectmode=tk.SINGLE, width=40, height=8, font=("Helvetica", 12))
        self.ham_listbox.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")

        ttk.Label(spam_frame, text="Spam Messages").grid(row=0, column=0, sticky="w")
        self.spam_listbox = tk.Listbox(spam_frame, selectmode=tk.SINGLE, width=40, height=8, font=("Helvetica", 12))
        self.spam_listbox.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        inbox_frame.columnconfigure(0, weight=1)
        inbox_frame.columnconfigure(1, weight=1)
        inbox_frame.rowconfigure(0, weight=1)

        ham_frame.columnconfigure(0, weight=1)
        ham_frame.rowconfigure(1, weight=1)

        spam_frame.columnconfigure(0, weight=1)
        spam_frame.rowconfigure(1, weight=1)

    def classify_message(self, mess):
        result = spam_classifier.classify(mess)
        
        if result == "ham":
            self.ham_messages.append(mess)
            self.ham_listbox.insert(tk.END, mess)
        elif result == "spam":
            self.spam_messages.append(mess)
            self.spam_listbox.insert(tk.END, mess)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    sms_spam = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])
    data_randomized = sms_spam.sample(frac=1, random_state=1)
    training_test_index = round(len(data_randomized) * 0.8)
    training_set = data_randomized[:training_test_index].reset_index(drop=True)

    spam_classifier = NaiveBayes(alpha=1)
    spam_classifier.train(training_set)

    mess = """
    WorldQuant BRAIN Việt Nam hân hạnh được tổ chức buổi gặp gỡ tháng 12/2023 dành riêng cho các bạn BRAIN consultant onboard trong năm 2023!
    """

    gmail_client = GmailClient()

    gmail_client.classify_message(mess)

    gmail_client.run()
