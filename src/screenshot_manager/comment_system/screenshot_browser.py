import io
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

from database_manager import (
    find_photo_by_id, get_tags, get_users,
    get_valid_screenshots
)
from screenshot_manager.comment_system.date_range_selector import \
    DateRangeSelector


class ScreenshotBrowser(tk.Toplevel):
    def __init__(self, comment_system_window):
        super().__init__(comment_system_window)
        self.title("Browse Photos")
        self.comment_system_window = comment_system_window

        self.screenshot_id = None
        self.photo = None

        self.tag_option = "All"
        self.user_option = "All"
        self.start_date = None
        self.end_date = None

        # Tags OptionMenu
        tags_label = tk.Label(self, text="Tags:")
        tags_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.tags_var = tk.StringVar()
        self.tags_optionmenu = ttk.OptionMenu(
                self,
                self.tags_var,
                "All",
                *["All"] + [f"{tag[0]}: {tag[1]}" for tag in get_tags()],
                command=self.update_tag_option
        )
        self.tags_optionmenu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Users OptionMenu
        users_label = tk.Label(self, text="Users:")
        users_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.users_var = tk.StringVar()
        self.users_optionmenu = ttk.OptionMenu(
                self,
                self.users_var,
                "All",
                *["All"] + [
                    f"{user[0]}: {user[1]}" for user in get_users()
                ],
                command=self.update_user_option
        )
        self.users_optionmenu.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Date Range Selector
        self.date_range_label = tk.Label(self, text="Selected Date Range: ")
        self.date_range_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.calendar_icon = ImageTk.PhotoImage(
                Image.open(r"resources\calendar_icon.jpg").resize((20, 20))
        )
        self.calendar_button = tk.Button(
                self,
                image=self.calendar_icon,
                command=self.open_date_range_selector
        )
        self.calendar_button.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        # Treeview
        self.screenshots_tree = ttk.Treeview(
                self,
                columns=(
                    "User ID", "Username", "Timestamp", "Tag ID", "Tag Name"
                )
        )
        self.screenshots_tree.grid(
                row=1, column=0, columnspan=6, padx=5, pady=5, sticky="nsew"
        )
        self.screenshots_tree.column("#0", width=90)
        self.screenshots_tree.heading("#0", text="Screenshot ID")
        self.screenshots_tree.column("User ID", width=75)
        self.screenshots_tree.heading("User ID", text="User ID")
        self.screenshots_tree.column("Username", width=75)
        self.screenshots_tree.heading("Username", text="Username")
        self.screenshots_tree.column("Timestamp", width=125)
        self.screenshots_tree.heading("Timestamp", text="Timestamp")
        self.screenshots_tree.column("Tag ID", width=50)
        self.screenshots_tree.heading("Tag ID", text="Tag ID")
        self.screenshots_tree.column("Tag Name", width=75)
        self.screenshots_tree.heading("Tag Name", text="Tag Name")
        self.screenshots_tree.bind("<<TreeviewSelect>>",
                                   self.update_photo_preview)

        # Configure vertical scrollbar
        self.tree_scroll_y = tk.Scrollbar(self, orient="vertical",
                                          command=self.screenshots_tree.yview)
        self.tree_scroll_y.grid(row=1, column=6, padx=5, pady=5, sticky="ns")
        self.screenshots_tree.configure(yscrollcommand=self.tree_scroll_y.set)

        # Selected Photo Preview
        self.photo_preview_label = tk.Label(
                self, text="[Selected Photo Preview]"
        )
        self.photo_preview_label.grid(
                row=1, column=7, padx=5, pady=5, sticky="nsew"
        )

        # Select Button
        select_button = tk.Button(
                self, text="Select", command=self.select_screenshot
        )
        select_button.grid(row=2, column=7, padx=5, pady=5, sticky="nsew")

        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=0)

        self.update_screenshots_tree()

    def select_screenshot(self):
        selected_item_id = self.screenshots_tree.selection()[0] \
            if self.screenshots_tree.selection() else None
        if selected_item_id:
            selected_item = self.screenshots_tree.item(selected_item_id)
            self.screenshot_id = selected_item["text"]
            self.comment_system_window.find_photo(self.screenshot_id)
            self.destroy()

    def update_photo_preview(self, event):
        selected_item = self.screenshots_tree.selection()[0] \
            if self.screenshots_tree.selection() else None
        if selected_item:
            self.screenshot_id = self.screenshots_tree.item(
                    selected_item, "text"
            )
            photo_blob = find_photo_by_id(self.screenshot_id)[0]
            photo = Image.open(io.BytesIO(photo_blob))
            photo.thumbnail((200, 200))
            self.photo = ImageTk.PhotoImage(photo)
            self.photo_preview_label.config(image=self.photo)
        else:
            self.photo_preview_label.config(image="")

    def open_date_range_selector(self):
        date_range_selector = DateRangeSelector(self.date_range_label)
        self.wait_window(date_range_selector)
        if date_range_selector.start_date and date_range_selector.end_date:
            self.start_date = date_range_selector.start_date
            self.end_date = date_range_selector.end_date
            self.update_screenshots_tree()

    def update_tag_option(self, value):
        self.tag_option = self.tags_var.get()
        self.update_screenshots_tree()

    def update_user_option(self, value):
        self.user_option = self.users_var.get()
        self.update_screenshots_tree()

    def update_screenshots_tree(self):
        valid_screenshots = get_valid_screenshots(
                self.tag_option,
                self.user_option,
                self.start_date,
                self.end_date
        )
        self.screenshots_tree.delete(*self.screenshots_tree.get_children())
        for screenshot in valid_screenshots:
            self.screenshots_tree.insert(
                    "",
                    "end",
                    text=screenshot[0],
                    values=(
                        screenshot[1],
                        screenshot[2],
                        screenshot[3],
                        screenshot[4],
                        screenshot[5]
                    )
            )
