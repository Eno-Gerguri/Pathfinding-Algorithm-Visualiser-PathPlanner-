import re
import tkinter as tk
from tkinter import messagebox

from user_authentication.authentication import create_user


class CreateUserWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Username label and entry
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Email label and entry
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password label and entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Confirm password label and entry
        self.confirm_password_label = tk.Label(self, text="Confirm Password:")
        self.confirm_password_label.grid(row=3, column=0, padx=10, pady=5,
                                         sticky="e")
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Register button
        self.register_button = tk.Button(self, text="Register",
                                         command=self.register_user)
        self.register_button.grid(row=4, column=0, columnspan=2, padx=10,
                                  pady=5, sticky="ew")

        # Switch to login button
        self.login_button = tk.Button(
                self,
                text="Login",
                command=lambda: self.controller.show_frame("LoginWindow")
        )
        self.login_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5,
                               sticky="ew")

    def validate_username(self, username):
        # Check if username is not empty
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return False
        # Additional checks can be added here, such as length requirements
        return True

    @staticmethod
    def validate_email(email):
        # Regular expression for validating email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Check if email matches the pattern
        if not re.match(email_regex, email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return False
        return True

    @staticmethod
    def validate_password(password):
        # Check if password is not empty
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return False
        # Check if password meets basic requirements
        if len(password) < 8:
            messagebox.showerror(
                    "Error", "Password must be at least 8 characters long"
            )
            return False
        if not any(char.isdigit() for char in password):
            messagebox.showerror(
                    "Error", "Password must contain at least one digit"
            )
            return False
        if not any(not char.isalnum() for char in password):
            messagebox.showerror(
                    "Error",
                    "Password must contain at least one special character"
            )
            return False
        return True

    @staticmethod
    def validate_password_confirmation(password, confirm_password):
        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return False
        return True

    def register_user(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate username, email, and password
        if (
                not self.validate_username(username) or
                not self.validate_email(email) or
                not self.validate_password(password) or
                not self.validate_password_confirmation(
                        password,
                        confirm_password
                )
        ):
            return

        # Perform user registration
        created_new_user = create_user(username, email, password)
        if created_new_user:
            messagebox.showinfo("Success", "User created")
            self.controller.show_frame("LoginWindow")
        else:
            messagebox.showerror("Error", "Username or Email already taken.")
