import tkinter as tk
from tkinter import messagebox
import pymysql

class BankManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("800x600")
        
        self.db_connect()

        title_label = tk.Label(self.root, text="Bank Management System", font=("Arial", 24, "bold"), bg="light blue")
        title_label.pack(side="top", fill="x")

        main_frame = tk.Frame(self.root, bd=10, relief="ridge")
        main_frame.place(x=200, y=100, width=400, height=400)

        open_ac_btn = tk.Button(main_frame, text="Open Account", command=self.open_account, font=("Arial", 16, "bold"))
        open_ac_btn.grid(row=0, column=0, padx=50, pady=20)

        deposit_btn = tk.Button(main_frame, text="Deposit", command=self.deposit, font=("Arial", 16, "bold"))
        deposit_btn.grid(row=1, column=0, padx=50, pady=20)

        withdraw_btn = tk.Button(main_frame, text="Withdraw", command=self.withdraw, font=("Arial", 16, "bold"))
        withdraw_btn.grid(row=2, column=0, padx=50, pady=20)

        balance_btn = tk.Button(main_frame, text="Check Balance", command=self.check_balance, font=("Arial", 16, "bold"))
        balance_btn.grid(row=3, column=0, padx=50, pady=20)

    def db_connect(self):
        """Establish a database connection."""
        try:
            self.con = pymysql.connect(host='localhost', user='root', password='Muskan123', database='bankdb')
            self.cur = self.con.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.root.destroy()

    def open_account(self):
        """Open a new bank account."""
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Open Account")
        self.new_window.geometry("400x400")

        name_label = tk.Label(self.new_window, text="User Name:", font=("Arial", 12))
        name_label.grid(row=0, column=0, padx=20, pady=10)
        self.name_entry = tk.Entry(self.new_window, width=30)
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)

        pw_label = tk.Label(self.new_window, text="Password:", font=("Arial", 12))
        pw_label.grid(row=1, column=0, padx=20, pady=10)
        self.pw_entry = tk.Entry(self.new_window, width=30, show="*")
        self.pw_entry.grid(row=1, column=1, padx=20, pady=10)

        confirm_pw_label = tk.Label(self.new_window, text="Confirm Password:", font=("Arial", 12))
        confirm_pw_label.grid(row=2, column=0, padx=20, pady=10)
        self.confirm_pw_entry = tk.Entry(self.new_window, width=30, show="*")
        self.confirm_pw_entry.grid(row=2, column=1, padx=20, pady=10)

        submit_btn = tk.Button(self.new_window, text="Submit", command=self.submit_account)
        submit_btn.grid(row=3, column=1, padx=20, pady=20)

    def submit_account(self):
        """Submit new account details."""
        user_name = self.name_entry.get()
        password = self.pw_entry.get()
        confirm_password = self.confirm_pw_entry.get()

        if password == confirm_password:
            try:
                self.cur.execute("INSERT INTO account (userName, userPW) VALUES (%s, %s)", (user_name, password))
                self.con.commit()
                messagebox.showinfo("Success", "Account opened successfully.")
                self.new_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error creating account: {e}")
        else:
            messagebox.showerror("Error", "Passwords do not match.")

    def deposit(self):
        """Deposit money to an account."""
        self.transact_window('Deposit')

    def withdraw(self):
        """Withdraw money from an account."""
        self.transact_window('Withdraw')

    def transact_window(self, action):
        """Create a transaction window for deposit or withdrawal."""
        self.transact_win = tk.Toplevel(self.root)
        self.transact_win.title(f"{action} Money")
        self.transact_win.geometry("400x300")

        name_label = tk.Label(self.transact_win, text="User Name:", font=("Arial", 12))
        name_label.grid(row=0, column=0, padx=20, pady=10)
        self.transact_name_entry = tk.Entry(self.transact_win, width=30)
        self.transact_name_entry.grid(row=0, column=1, padx=20, pady=10)

        amount_label = tk.Label(self.transact_win, text=f"Amount to {action}:", font=("Arial", 12))
        amount_label.grid(row=1, column=0, padx=20, pady=10)
        self.transact_amount_entry = tk.Entry(self.transact_win, width=30)
        self.transact_amount_entry.grid(row=1, column=1, padx=20, pady=10)

        transact_btn = tk.Button(self.transact_win, text=action, command=lambda: self.perform_transaction(action))
        transact_btn.grid(row=2, column=1, padx=20, pady=20)

    def perform_transaction(self, action):
        """Perform deposit or withdrawal."""
        user_name = self.transact_name_entry.get()
        amount = float(self.transact_amount_entry.get())

        try:
            self.cur.execute("SELECT balance FROM account WHERE userName=%s", (user_name,))
            data = self.cur.fetchone()
            if data:
                current_balance = data[0]
                if action == 'Deposit':
                    new_balance = current_balance + amount
                elif action == 'Withdraw':
                    if current_balance >= amount:
                        new_balance = current_balance - amount
                    else:
                        messagebox.showerror("Error", "Insufficient funds.")
                        return
                self.cur.execute("UPDATE account SET balance=%s WHERE userName=%s", (new_balance, user_name))
                self.con.commit()
                messagebox.showinfo("Success", f"{action} completed successfully.")
                self.transact_win.destroy()
            else:
                messagebox.showerror("Error", "User not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Transaction failed: {e}")

    def check_balance(self):
        """Check the balance of a bank account."""
        self.balance_window = tk.Toplevel(self.root)
        self.balance_window.title("Check Balance")
        self.balance_window.geometry("400x200")

        name_label = tk.Label(self.balance_window, text="User Name:", font=("Arial", 12))
        name_label.grid(row=0, column=0, padx=20, pady=10)
        self.balance_name_entry = tk.Entry(self.balance_window, width=30)
        self.balance_name_entry.grid(row=0, column=1, padx=20, pady=10)

        check_btn = tk.Button(self.balance_window, text="Check", command=self.show_balance)
        check_btn.grid(row=1, column=1, padx=20, pady=20)

    def show_balance(self):
        """Display the account balance."""
        user_name = self.balance_name_entry.get()

        try:
            self.cur.execute("SELECT balance FROM account WHERE userName=%s", (user_name,))
            data = self.cur.fetchone()
            if data:
                balance = data[0]
                messagebox.showinfo("Balance", f"Account balance: ${balance}")
            else:
                messagebox.showerror("Error", "User not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving balance: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagement(root)
    root.mainloop()
