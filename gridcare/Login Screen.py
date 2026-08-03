#Building the login screen
from logging import root
import tkinter as tk
from tkinter import ttk, messagebox


"""def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "password":
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password")

root = tk.Tk()
root.title("Login Screen")

label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

button_login = tk.Button(root, text="Login", command=login)
button_login.pack()

root.mainloop()"""

class LoginWindow(tk.Frame):
    def __init__(self, master, on_success):

        super().__init__(master)
        self.on_success = on_success
        master.title("GridCare-Lite - Login")

        ttk.Label(self, text = "Username:").grid(row=0, column=0, padx=8, pady=8, sticky = "e")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=8, pady=8, sticky = "e")

        ttk.Label(self, text = "Password:").grid(row=1, column=0, padx=8, pady=8, sticky = "e")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=8, pady=8, sticky = "e")

        ttk.Button(self, text="Login", command=self.attempt_login).grid(row=2, column=0, columnspan=2, pady=10)
        self.pack(padx=20, pady=20)
        
    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Login Failed", "Enter both a username and password.")
            return
            # TODO check against the users table
            self.on_success(username)
    

        
class Dashboard(tk.Frame):
     def __init__(self, master, username):
      super().__init__(master)
      master.title(f"GridCare-Lite — Dashboard ({username})")
      ttk.Label(self, text=f"Welcome, {username}!", font=("Segoe UI", 14)).pack(pady=20)
      self.pack(fill="both", expand=True)
        
        
def main():
    root = tk.Tk()

    def show_dashboard(username):
        for widget in root.winfo_children():
            widget.destroy()
        Dashboard(root, username)

    LoginWindow(root, on_success=show_dashboard)

    root.mainloop()

if __name__ == "__main__":
    main()