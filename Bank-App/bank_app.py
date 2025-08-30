import customtkinter as ctk
import hashlib
from datetime import datetime
import os

# Hashing passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check user data (read file)
def load_all_user_data():
    users = {}
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as f:
            for line in f:
                username, password, role, balance = line.strip().split(',')
                users[username] = {
                    "password": password,
                    "role": role,
                    "balance": float(balance)
                }
    return users

# Save data of new username or password
def save_user(users):
    with open("user.txt", "w") as f:
        for username, data in users.items():
            f.write(f"{username},{data['password']},{data['role']},{data['balance']}\n")

# Check deposit and withdraw then make transaction record
def transaction_records(username, action, balance):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("transactions.txt", "a") as f:
        f.write(f"{time} | {username} | {action} | ${balance:.2f}\n")

# App class
class BankApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BANK APP")
        self.geometry("600x600+450+45")
        self.iconbitmap("bank.ico") 
        self.user = load_all_user_data()
        self.current_user = None
        self.current_role = None
        self.show_login()
    
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- LOGIN PAGE ---
    def show_login(self):
        self.clear()
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Login", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        self.login_user_entry = ctk.CTkEntry(frame, placeholder_text='username')
        self.login_user_entry.pack(pady=10)
        self.login_pass_entry = ctk.CTkEntry(frame, placeholder_text='Password', show='*')
        self.login_pass_entry.pack(pady=10)
        ctk.CTkButton(frame, text="Login", command=self.login_user).pack(pady=10)
        ctk.CTkButton(frame, text="Go to Signup", command=self.show_signup).pack(pady=10)

    def login_user(self):
        username = self.login_user_entry.get()
        password = hash_password(self.login_pass_entry.get())
        if username in self.user and password == self.user[username]['password']:
            self.current_user = username
            self.current_role = self.user[username]['role']
            self.show_dashboard()
        else:
            self.clear()
            ctk.CTkLabel(self, text="Invalid credentials", text_color="red").pack(pady=10)
            ctk.CTkButton(self, text="Back", command=self.show_login).pack(pady=5)

    # --- SIGNUP PAGE ---
    def show_signup(self):
        self.clear()
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Signup", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        self.signup_user_entry = ctk.CTkEntry(frame, placeholder_text='username')
        self.signup_user_entry.pack(pady=10)
        self.signup_pass_entry = ctk.CTkEntry(frame, placeholder_text='Password', show='*')
        self.signup_pass_entry.pack(pady=10)
        ctk.CTkButton(frame, text="Create Account", command=self.show_user).pack(pady=10)
        ctk.CTkButton(frame, text="Back to Login", command=self.show_login).pack(pady=10)

    def show_user(self):
        username = self.signup_user_entry.get()
        password = hash_password(self.signup_pass_entry.get())
        if username in self.user:
            ctk.CTkLabel(self, text="Username already exists", text_color="red").pack(pady=10)
            ctk.CTkButton(self, text="Back", command=self.show_signup).pack(pady=10)
        else:
            self.user[username] = {
                'password': password,
                'role': "member",
                'balance': 0.0
            }
            save_user(self.user)
            self.show_login()

    # --- DASHBOARD ---
    def show_dashboard(self):
        self.clear()
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text=f"Welcome, {self.current_user}!", font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkButton(frame, text="Check Balance", command=self.show_balance).pack(pady=5)
        ctk.CTkButton(frame, text="Deposit", command=self.deposit_money).pack(pady=5)
        ctk.CTkButton(frame, text="Withdraw", command=self.withdraw_money).pack(pady=5)
        ctk.CTkButton(frame, text="Transaction History", command=self.show_history).pack(pady=5)

        if self.current_role == "head":
            ctk.CTkButton(frame, text="Manage Users", command=self.manage_users).pack(pady=5)

        ctk.CTkButton(frame, text="Logout", command=self.show_login).pack(pady=10)
        ctk.CTkLabel(frame, text="Delete account or reset username/password:", font=ctk.CTkFont(size=14)).pack(pady=10)
        ctk.CTkLabel(frame, text="Contact: xyz@gmail.com", font=ctk.CTkFont(size=14)).pack(pady=5)

    # --- BALANCE SCREEN ---
    def show_balance(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        bal = self.user[self.current_user]["balance"]
        ctk.CTkLabel(frame, text="Your Balance", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkLabel(frame, text=f"Balance: ${bal:.2f}", font=ctk.CTkFont(size=16)).pack(pady=10)

        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack(pady=10)

    # --- DEPOSIT ---
    def deposit_money(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Enter deposit amount:").pack(pady=10)
        entry = ctk.CTkEntry(frame)
        entry.pack(pady=10)
        
        def confirm():
            try:
                amount = float(entry.get())
                if amount > 0:
                    self.user[self.current_user]["balance"] += amount
                    save_user(self.user)
                    transaction_records(self.current_user, "Deposit", amount)
                    self.show_balance()
                else:
                    ctk.CTkLabel(frame, text="Invalid amount", text_color="red").pack()
            except ValueError:
                ctk.CTkLabel(frame, text="Enter number only", text_color="red").pack()
        
        ctk.CTkButton(frame, text="Confirm", command=confirm).pack(pady=10)
        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack(pady=10)

    # --- WITHDRAW ---
    def withdraw_money(self):
        self.clear()
        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Enter withdrawal amount:").pack(pady=10)
        entry = ctk.CTkEntry(frame)
        entry.pack(pady=10)

        def confirm():
            try:
                amount = float(entry.get())
                if 0 < amount <= self.user[self.current_user]["balance"]:
                    self.user[self.current_user]["balance"] -= amount
                    save_user(self.user)
                    transaction_records(self.current_user, "Withdraw", amount)
                    self.show_balance()
                else:
                    ctk.CTkLabel(frame, text="Not enough balance", text_color="red").pack(pady=10)
            except ValueError:
                ctk.CTkLabel(frame, text="Enter number only", text_color="red").pack(pady=10)

        ctk.CTkButton(frame, text="Confirm", command=confirm).pack(pady=10)
        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack(pady=10)

    # --- TRANSACTION HISTORY ---
    def show_history(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        box = ctk.CTkTextbox(frame, width=440, height=280)
        box.pack(pady=10)
        if os.path.exists("transactions.txt"):
            with open("transactions.txt", "r") as f:
                for line in f:
                    if f"| {self.current_user} |" in line:
                        box.insert("end", line)
        else:
            box.insert("end", "No transactions yet.")
        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack(pady=10)

    # --- HEAD: MANAGE USERS ---
    def manage_users(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text="User Management", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        # Target Username
        ctk.CTkLabel(frame, text="Target Username:").pack(pady=5)
        user_entry = ctk.CTkEntry(frame)
        user_entry.pack(padx=10)

        # New Username
        ctk.CTkLabel(frame, text="New Username (leave blank if no change):").pack(pady=5)
        new_user_entry = ctk.CTkEntry(frame)
        new_user_entry.pack(padx=10)

        # New Password
        ctk.CTkLabel(frame, text="New Password (leave blank if no change):").pack(pady=5)
        new_pass_entry = ctk.CTkEntry(frame, show="*")
        new_pass_entry.pack(padx=10)

        # New Balance
        ctk.CTkLabel(frame, text="New Balance (leave blank if no change):").pack(pady=5)
        bal_entry = ctk.CTkEntry(frame)
        bal_entry.pack(padx=10)

        # New Role
        ctk.CTkLabel(frame, text="New Role (member/head, leave blank if no change):").pack(pady=5)
        role_entry = ctk.CTkEntry(frame)
        role_entry.pack(padx=10)

        def update():
            u = user_entry.get()
            if u not in self.user:
                ctk.CTkLabel(frame, text="User not found", text_color="red").pack(pady=10)
                return

            # Username change
            new_username = new_user_entry.get().strip()
            if new_username and new_username not in self.user:
                self.user[new_username] = self.user.pop(u)
                u = new_username
            elif new_username and new_username in self.user:
                ctk.CTkLabel(frame, text="New username already exists", text_color="red").pack(pady=10)
                return

            # Password change
            new_pass = new_pass_entry.get()
            if new_pass:
                self.user[u]["password"] = hash_password(new_pass)

            # Balance change
            new_bal = bal_entry.get()
            if new_bal:
                try:
                    self.user[u]["balance"] = float(new_bal)
                except ValueError:
                    ctk.CTkLabel(frame, text="Invalid balance", text_color="red").pack(pady=10)
                    return

            # Role change
            new_role = role_entry.get().strip().lower()
            if new_role in ["member", "head"]:
                self.user[u]["role"] = new_role
            elif new_role:
                ctk.CTkLabel(frame, text="Invalid role (use 'member' or 'head')", text_color="red").pack(pady=10)
                return

            save_user(self.user)
            ctk.CTkLabel(frame, text="User updated successfully!", text_color="green").pack(padx=10)

        ctk.CTkButton(frame, text="Update User", command=update).pack(pady=10)
        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack(pady=10)

# Run the app
if __name__ == "__main__":
    BankApp().mainloop()
