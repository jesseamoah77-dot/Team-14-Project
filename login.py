"""
login.py
GridCare-Lite - Login screen with real password security
"""

import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt

from database import init_db


def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_password, stored_hash):
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash)


def add_user(username, plain_password, role, db_path='gridcare.db'):
    conn = init_db(db_path)
    cur = conn.cursor()
    password_hash = hash_password(plain_password)
    try:
        cur.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            (username, password_hash, role)
        )
        conn.commit()
        print(f"User '{username}' created with role '{role}'.")
    except Exception as e:
        print(f"Could not create user '{username}': {e}")
    finally:
        conn.close()


class LoginWindow(tk.Frame):
    def __init__(self, master, on_success, db_path='gridcare.db'):
        super().__init__(master)
        self.on_success = on_success
        self.db_path = db_path
        self.master = master
        master.title('GridCare-Lite - Login')

        ttk.Label(self, text='Username:').grid(row=0, column=0, padx=8, pady=8, sticky='e')
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(self, text='Password:').grid(row=1, column=0, padx=8, pady=8, sticky='e')
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Button(self, text='Log In', command=self.attempt_login).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        self.pack(padx=20, pady=20)

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

        if row is None:
            messagebox.showerror('Login Failed', 'No account found with that username.')
            return

        user_id, stored_hash, role = row

        if check_password(password, stored_hash):
            self.on_success(user_id, username, role)
        else:
            messagebox.showerror('Login Failed', 'Incorrect password.')


class PlaceholderDashboard(tk.Frame):
    def __init__(self, master, username, role):
        super().__init__(master)
        master.title(f'GridCare-Lite - {role.title()} Dashboard ({username})')
        ttk.Label(
            self,
            text=f"Logged in as '{username}'\nRole: {role}\n\n"
                 f"(Replace this screen with the real dashboard for this role)"
        ).pack(padx=40, pady=40)
        self.pack()

def main():
    root = tk.Tk()

    def show_dashboard(user_id, username, role):
        for widget in root.winfo_children():
            widget.destroy()
        from dashboard import OutageDashboard
        OutageDashboard(root, user_id, username, role)

    LoginWindow(root, on_success=show_dashboard)
    root.mainloop()


if __name__ == '__main__':
    main()
