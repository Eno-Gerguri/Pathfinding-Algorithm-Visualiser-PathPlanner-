import tkinter as tk

from user_authentication.create_user_window import CreateUserWindow
from user_authentication.login_window import LoginWindow


class ParentLoginWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Login System")

        self.user_id = None

        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginWindow, CreateUserWindow):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginWindow")

    def show_frame(self, window_name):
        frame_names = {
            "LoginWindow": LoginWindow,
            "CreateUserWindow": CreateUserWindow
        }
        window = frame_names[window_name]
        frame = self.frames[window]
        frame.tkraise()
