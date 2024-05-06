import tkinter as tk
from tkinter import messagebox
import pickle
from accounts import Account, SavingsAccount

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Account Manager")
        self.geometry("400x300")
        self.load_accounts()  # Load accounts from file
        self.create_login_widgets()  # Initialize the login interface

    def load_accounts(self):
        try:
            with open('accounts.pkl', 'rb') as f:
                self.accounts = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.accounts = {}

    def save_accounts(self):
        with open('accounts.pkl', 'wb') as f:
            pickle.dump(self.accounts, f)

    def create_login_widgets(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack()
        tk.Label(self.login_frame, text="Account Name").pack(pady=(10, 0))
        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.pack(pady=(0, 10))

        tk.Label(self.login_frame, text="Account PIN").pack(pady=(10, 0))
        self.account_pin_entry = tk.Entry(self.login_frame, show="*")
        self.account_pin_entry.pack(pady=(0, 10))

        self.login_button = tk.Button(self.login_frame, text="Login or Register", command=self.login_or_register)
        self.login_button.pack(pady=20)

    def login_or_register(self):
        name = self.name_entry.get().strip()
        pin_input = self.account_pin_entry.get().strip()
        if len(pin_input) != 4 or not pin_input.isdigit():
            messagebox.showerror("Error", "Invalid PIN")
            return

        pin = int(pin_input)
        account_key = (pin, name)
        if account_key not in self.accounts:
            self.accounts[account_key] = Account(name, pin)  # Create new account
            self.save_accounts()  # Save the new account to file
        self.account = self.accounts[account_key]
        self.login_frame.pack_forget()  # Remove the login frame
        self.create_widgets()  # Add transaction widgets
        self.update_idletasks()  # Update the GUI

    def create_widgets(self):
        self.transaction_frame = tk.Frame(self)
        self.transaction_frame.pack()

        self.deposit_amount_entry = tk.Entry(self.transaction_frame)
        self.deposit_amount_entry.pack(pady=10)

        self.deposit_button = tk.Button(self.transaction_frame, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=10)

        self.withdraw_amount_entry = tk.Entry(self.transaction_frame)
        self.withdraw_amount_entry.pack(pady=10)

        self.withdraw_button = tk.Button(self.transaction_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.balance_label = tk.Label(self.transaction_frame, text=f"Balance: ${self.account.get_balance():.2f}")
        self.balance_label.pack(pady=20)

    def deposit(self):
        try:
            amount = float(self.deposit_amount_entry.get())
            if self.account.deposit(amount):
                self.update_balance()
                messagebox.showinfo("Success", "Deposit Successful")
                self.save_accounts()
            else:
                messagebox.showerror("Error", "Invalid deposit amount")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def withdraw(self):
        try:
            amount = float(self.withdraw_amount_entry.get())
            if self.account.withdraw(amount):
                self.update_balance()
                messagebox.showinfo("Success", "Withdrawal Successful")
                self.save_accounts()
            else:
                messagebox.showerror("Error", "Invalid withdrawal amount or insufficient funds")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.account.get_balance():.2f}")

if __name__ == '__main__':
    app = BankApp()
    app.mainloop()
