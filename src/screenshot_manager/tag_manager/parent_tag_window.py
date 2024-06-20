import tkinter as tk

from screenshot_manager.tag_manager.create_new_tag_window import CreateNewTagWindow
from screenshot_manager.tag_manager.select_tag_window import SelectTagWindow


class ParentTagWindow(tk.Tk):
    def __init__(self, tags):
        tk.Tk.__init__(self)
        self.title("Tag System")
        self.tags = tags

        self.selected_tag = None

        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for F in (SelectTagWindow, CreateNewTagWindow):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SelectTagWindow")

    def show_frame(self, window_name):
        frame_names = {
            "SelectTagWindow": SelectTagWindow,
            "CreateNewTagWindow": CreateNewTagWindow
        }
        window = frame_names[window_name]
        frame = self.frames[window]
        frame.tkraise()

    def update_tag_menu(self):
        tag_menu = self.frames[SelectTagWindow].tag_dropdown["menu"]
        new_tag = self.tags[-1]
        tag_menu.add_command(
                label=new_tag,
                command=tk._setit(
                        self.frames[SelectTagWindow].currently_selected_tag,
                        new_tag
                )
        )
