import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import authenticate, register_user
from logger import log
from deepseek_client import get_fun_fact


class LoginWindow:
    def __init__(self, root):
        """Initializes the login window UI and displays a fun fact."""
        self.root = root
        self.root.title("Champions League Login")
        self.root.geometry("420x340")
        self.root.configure(bg="#1b1f3b")

        tk.Label(root, text="⚽ Champions League Simulator",
                 font=("Helvetica", 16, "bold"), fg="white", bg="#1b1f3b").pack(pady=12)

        tk.Label(root, text="Username:", fg="white", bg="#1b1f3b",
                 font=("Helvetica", 11)).pack(pady=3)
        self.username_entry = tk.Entry(root, width=30, font=("Helvetica", 11))
        self.username_entry.pack(pady=3)

        tk.Label(root, text="Password:", fg="white", bg="#1b1f3b",
                 font=("Helvetica", 11)).pack(pady=3)
        self.password_entry = tk.Entry(root, width=30, show="*", font=("Helvetica", 11))
        self.password_entry.pack(pady=3)

        btn_style = {"font": ("Helvetica", 11, "bold"), "width": 12, "bg": "#4e73df", "fg": "white"}

        tk.Button(root, text="Login", command=self.login, **btn_style).pack(pady=8)
        tk.Button(root, text="Register", command=self.register, **btn_style).pack(pady=5)

        fact = get_fun_fact()
        self.fact_label = tk.Label(root, text=f"Fun Fact: {fact}", wraplength=350, fg="#c7d5ff",
                                   bg="#1b1f3b", font=("Helvetica", 10, "italic"))
        self.fact_label.pack(pady=12)

        self.user = None

    def login(self):
        """Authenticates the user and closes the window on success."""
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
        """Creates a new user account after validating age and password."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Enter username and password.")
            return

        age = simpledialog.askinteger("Age", "Enter your age:")
        if age is None:
            return

        if age < 21:
            messagebox.showerror("Error", "You must be 21 or older.")
            log(f"Rejected registration: {username} ({age})")
            return

        result = register_user(username, password, age)

        if result == "weak_password":
            messagebox.showerror("Error", "Password must contain letters, digits, and be at least 8 characters.")
            return

        if result == "username_taken":
            messagebox.showerror("Error", "Username already taken.")
            return

        if result == "success":
            messagebox.showinfo("Success", "Account created!")
            log(f"User registered: {username}")
