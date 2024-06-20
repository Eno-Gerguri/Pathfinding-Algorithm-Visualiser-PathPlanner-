import tkinter as tk
from tkinter import messagebox


class SelectTagWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.currently_selected_tag = tk.StringVar()
        self.currently_selected_tag.set(
                self.controller.tags[0] if self.controller.tags else ""
        )

        label = tk.Label(self, text="Select Tag:")
        label.grid(row=0, column=0, padx=10, pady=5)

        self.tag_dropdown = tk.OptionMenu(
                self,
                self.currently_selected_tag,
                self.currently_selected_tag.get(),
                *self.controller.tags[1:]
        )
        self.tag_dropdown.grid(row=0, column=1, padx=10, pady=5)

        select_button = tk.Button(self, text="Select Tag",
                                  command=self.select_tag)
        select_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        create_new_tag_button = tk.Button(
                self,
                text="Create New Tag",
                command=lambda: self.controller.show_frame(
                        "CreateNewTagWindow"
                )
        )
        create_new_tag_button.grid(
                row=2, column=0, columnspan=2, padx=10, pady=5
        )

    def select_tag(self):
        tag_name = self.currently_selected_tag.get()
        if tag_name:
            messagebox.showinfo("Success", "Tag selected")
            self.controller.selected_tag = tag_name
            self.controller.destroy()
        else:
            messagebox.showerror("Error", "Tag name cannot be empty")
