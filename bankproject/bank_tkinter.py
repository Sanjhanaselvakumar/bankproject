import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Database connection setup
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Deena@2508",
            database="bank_db"
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

# Main Banking System GUI
class BankingSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("400x400")
        self.connection = connect_to_database()
        if not self.connection:
            self.root.destroy()
            return
        self.cursor = self.connection.cursor()
        self.user_id = None
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to the Banking System!", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Log In as Existing User", command=self.login_screen, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Add New User", command=self.add_user_screen, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.exit_application, width=30, height=2).pack(pady=10)

    def login_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Log In", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter User ID:", font=("Arial", 12)).pack(pady=5)
        user_id_entry = tk.Entry(self.root, width=30)
        user_id_entry.pack(pady=5)
        tk.Button(self.root, text="Log In", command=lambda: self.login_user(user_id_entry.get()), width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    def login_user(self, user_id):
        try:
            user_id = int(user_id)
            self.cursor.execute("SELECT name, age, gender, balance FROM users WHERE id = %s", (user_id,))
            user_data = self.cursor.fetchone()
            if user_data:
                self.user_id = user_id
                self.name, self.age, self.gender, self.balance = user_data
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "User not found!")
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID!")

    def user_dashboard(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {self.name}!", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Deposit Money", command=self.deposit_screen, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw_screen, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="View Balance", command=self.view_balance, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Log Out", command=self.create_main_menu, width=30, height=2).pack(pady=10)

    def deposit_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Deposit Money", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter Amount:", font=("Arial", 12)).pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30)
        amount_entry.pack(pady=5)
        tk.Button(self.root, text="Deposit", command=lambda: self.deposit_money(amount_entry.get()), width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.user_dashboard, width=20).pack(pady=10)

    def deposit_money(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount
                self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (self.balance, self.user_id))
                self.connection.commit()
                messagebox.showinfo("Success", f"Deposited {amount} successfully!")
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid deposit amount!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")

    def withdraw_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Withdraw Money", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter Amount:", font=("Arial", 12)).pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30)
        amount_entry.pack(pady=5)
        tk.Button(self.root, text="Withdraw", command=lambda: self.withdraw_money(amount_entry.get()), width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.user_dashboard, width=20).pack(pady=10)

    def withdraw_money(self, amount):
        try:
            amount = float(amount)
            if amount > self.balance:
                messagebox.showerror("Error", "Insufficient funds!")
            elif amount > 0:
                self.balance -= amount
                self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (self.balance, self.user_id))
                self.connection.commit()
                messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid withdrawal amount!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")

    def view_balance(self):
        messagebox.showinfo("Balance", f"Current Balance: {self.balance}")

    def add_user_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Add New User", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Name:", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(self.root, width=30)
        name_entry.pack(pady=5)
        tk.Label(self.root, text="Age:", font=("Arial", 12)).pack(pady=5)
        age_entry = tk.Entry(self.root, width=30)
        age_entry.pack(pady=5)
        tk.Label(self.root, text="Gender:", font=("Arial", 12)).pack(pady=5)
        gender_entry = tk.Entry(self.root, width=30)
        gender_entry.pack(pady=5)
        tk.Label(self.root, text="Initial Deposit:", font=("Arial", 12)).pack(pady=5)
        deposit_entry = tk.Entry(self.root, width=30)
        deposit_entry.pack(pady=5)
        tk.Button(self.root, text="Add User", command=lambda: self.add_user(name_entry.get(), age_entry.get(), gender_entry.get(), deposit_entry.get()), width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    def add_user(self, name, age, gender, initial_deposit):
        try:
            age = int(age)
            initial_deposit = float(initial_deposit)
            if initial_deposit >= 0:
                self.cursor.execute("INSERT INTO users (name, age, gender, balance) VALUES (%s, %s, %s, %s)", (name, age, gender, initial_deposit))
                self.connection.commit()
                messagebox.showinfo("Success", "New user added successfully!")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Invalid deposit amount!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    def exit_application(self):
        self.cursor.close()
        self.connection.close()
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystemGUI(root)
    root.mainloop()