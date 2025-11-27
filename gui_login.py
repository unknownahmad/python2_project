import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import authenticate, register_user
from logger import log

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")

        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", width=12, command=self.login).pack(pady=8)
        tk.Button(root, text="Register", width=12, command=self.register).pack(pady=5)

        self.user = None

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Enter username and password.")
            return

        user = authenticate(username, password)

        if user is None:
            messagebox.showerror("Error", "Incorrect username or password.")
            log(f"Failed login: {username}")
            return

        messagebox.showinfo("Success", f"Welcome {username}")
        log(f"User logged in: {username}")
        self.user = user
        self.root.destroy()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Enter username and password to register.")
            return

        age = simpledialog.askinteger("Age", "Enter your age:")
        if age is None:
            return

        if age < 21:
            messagebox.showerror("Error", "You must be 21 or older to register.")
            log(f"Rejected underage registration: {username} ({age})")
            return

        result = register_user(username, password, age)

        if result == "weak_password":
            messagebox.showerror("Error", "Password must contain letters, digits, and be at least 8 characters.")
            return

        if result == "username_taken":
            messagebox.showerror("Error", "Username already taken.")
            return

        if result == "success":
            messagebox.showinfo("Success", "Account created.")
            log(f"User registered: {username}")
