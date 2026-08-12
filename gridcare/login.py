"""
login.py
GridCare-Lite - User Authentication Interface

Handles user login, password verification (bcrypt), and role-based 
navigation into the main Outage Dashboard.
"""

import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
from database import init_db

# Ensure paths resolve correctly relative to this script's folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'gridcare.db')


def hash_password(plain_password: str) -> str:
    """Hashes a plain text password and returns a string for SQLite storage."""
    hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def check_password(plain_password: str, stored_hash) -> bool:
    """Verifies a plain text password against a stored bcrypt hash."""
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash)


def add_user(username, password, role='technician', db_path=DEFAULT_DB_PATH):
    """Helper function to insert users safely into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    hashed = hash_password(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )
        conn.commit()
        print(f" • User '{username}' created successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f" • User '{username}' already exists. Skipping.")
        return False
    finally:
        conn.close()


class LoginWindow(ttk.Frame):
    """Modern, centered login screen interface."""

    def __init__(self, master, on_success, db_path=DEFAULT_DB_PATH):
        super().__init__(master, padding=25)
        self.master = master
        self.on_success = on_success
        self.db_path = db_path

        self.master.title('GridCare-Lite | Login')
        self.master.resizable(False, False)

        # Build Form UI
        self._create_widgets()
        self.pack(expand=True)

        # Bind Enter key to submit login
        self.master.bind('<Return>', lambda event: self.attempt_login())

    def _create_widgets(self):
        # Title Header
        title_label = ttk.Label(
            self, 
            text="GridCare-Lite", 
            font=("Segoe UI", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Username Input
        ttk.Label(self, text='Username:', font=("Segoe UI", 10)).grid(
            row=1, column=0, padx=(0, 8), pady=8, sticky='e'
        )
        self.username_entry = ttk.Entry(self, width=25)
        self.username_entry.grid(row=1, column=1, pady=8)
        self.username_entry.focus()  # Focus cursor on startup

        # Password Input
        ttk.Label(self, text='Password:', font=("Segoe UI", 10)).grid(
            row=2, column=0, padx=(0, 8), pady=8, sticky='e'
        )
        self.password_entry = ttk.Entry(self, show='•', width=25)
        self.password_entry.grid(row=2, column=1, pady=8)

        # Login Button
        login_btn = ttk.Button(
            self, 
            text='Log In', 
            command=self.attempt_login
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=(15, 0))

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror('Login Failed', 'Please enter both a username and password.')
            return

        conn = init_db(self.db_path)
        cur = conn.cursor()
        cur.execute('SELECT user_id, password_hash, role FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        conn.close()

        # Generic failure message for security
        if row is None:
            messagebox.showerror('Login Failed', 'Invalid username or password.')
            return

        user_id, stored_hash, role = row

        if check_password(password, stored_hash):
            self.master.unbind('<Return>')  # Remove shortcut after login
            self.on_success(user_id, username, role)
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password.')


def center_window(window, width=360, height=260):
    """Centers the Tkinter window on screen."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def main():
    root = tk.Tk()
    center_window(root, 360, 260)

    def show_dashboard(user_id, username, role):
        for widget in root.winfo_children():
            widget.destroy()

        from dashboard import OutageDashboard
        
        root.resizable(True, True)
        center_window(root, 850, 500)
        OutageDashboard(root, user_id, username, role)

    LoginWindow(root, on_success=show_dashboard)
    root.mainloop()


if __name__ == '__main__':
    main()