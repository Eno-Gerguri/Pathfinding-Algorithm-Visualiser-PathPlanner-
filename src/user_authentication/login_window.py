import tkinter as tk
from tkinter import messagebox

from user_authentication.authentication import verify_login


class LoginWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Username label and entry
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password label and entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Login button
        self.login_button = tk.Button(
                self, text="Login", command=self.login, width=10
        )
        self.login_button.grid(
                row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew"
        )

        # Switch to create new user button
        self.signup_button = tk.Button(
                self,
                text="Sign Up",
                command=lambda: controller.show_frame("CreateUserWindow"),
                width=10
        )
        self.signup_button.grid(
                row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew"
        )

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(
                    "Error",
                    "Please enter both username and password"
            )
            return

        user_id = verify_login(username, password)
        if user_id:
            messagebox.showinfo("Success", "Login successful")
            self.controller.user_id = user_id
            self.controller.destroy()
        else:
            messagebox.showerror(
                    "Error", "Invalid username or password"
            )
