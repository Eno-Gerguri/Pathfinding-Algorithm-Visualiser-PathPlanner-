import tkinter as tk
from tkinter import messagebox

from database_manager import add_tag


class CreateNewTagWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Tag name label and entry
        self.tag_name_label = tk.Label(self, text="Tag Name:")
        self.tag_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.tag_name_entry = tk.Entry(self)
        self.tag_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Create tag button
        self.create_tag_button = tk.Button(self, text="Create Tag",
                                           command=self.create_tag)
        self.create_tag_button.grid(row=1, column=0, columnspan=2, padx=10,
                                    pady=5, sticky="ew")

        # Switch to select tag button
        self.select_tag_button = tk.Button(
                self,
                text="Select Tag",
                command=lambda: self.controller.show_frame("SelectTagWindow"))
        self.select_tag_button.grid(row=2, column=0, columnspan=2, padx=10,
                                    pady=5, sticky="ew")

    def create_tag(self):
        tag_name = self.tag_name_entry.get()

        if not tag_name:
            messagebox.showerror("Error", "Tag name cannot be empty")
            return

        created_new_tag = add_tag(tag_name)
        if created_new_tag:
            self.controller.tags.append(tag_name)
            self.controller.update_tag_menu()
            messagebox.showinfo("Success", "Tag created")
            self.controller.show_frame("SelectTagWindow")
