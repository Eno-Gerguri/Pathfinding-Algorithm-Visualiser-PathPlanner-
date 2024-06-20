import io
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

from database_manager import find_photo_by_id, upload_comment
from screenshot_manager.comment_system.screenshot_browser import \
    ScreenshotBrowser


class MakeNewCommentWindow(tk.Tk):
    def __init__(self, user_id, screenshot_id=None):
        super().__init__()
        self.title("Add New Comment")

        self.user_id = user_id
        self.screenshot_id = screenshot_id
        self.screenshot_photo = None

        # Upper Left Section
        upper_left_frame = tk.Frame(self)
        upper_left_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")
        self.grid_rowconfigure(0,
                               weight=1)
        self.grid_columnconfigure(0,
                                  weight=1)

        photo_id_label = tk.Label(upper_left_frame, text="Photo ID:")
        photo_id_label.grid(row=0, column=0, padx=5, pady=5)
        vcmd = (self.register(self.validate_numeric_input), '%P')
        self.photo_id_entry = tk.Entry(
                upper_left_frame, validate="key", validatecommand=vcmd
        )
        self.photo_id_entry.grid(row=0, column=1, padx=5, pady=5)
        find_button = tk.Button(
                upper_left_frame, text="Find", command=self.find_photo
        )
        find_button.grid(row=0, column=2, padx=5, pady=5)

        selected_photo_label = tk.Label(
                upper_left_frame, text="Selected Photo:"
        )
        selected_photo_label.grid(row=1, column=0, padx=5, pady=5)
        self.selected_photo_label = tk.Label(upper_left_frame, text="")
        self.selected_photo_label.grid(row=1, column=1, padx=5, pady=5)

        time_taken_label = tk.Label(upper_left_frame, text="Time Taken:")
        time_taken_label.grid(row=2, column=0, padx=5, pady=5)
        self.time_taken_label = tk.Label(upper_left_frame, text="timestamp")
        self.time_taken_label.grid(row=2, column=1, padx=5, pady=5)
        browse_button = tk.Button(
                upper_left_frame,
                text="Browse...",
                command=self.browse_screenshot
        )
        browse_button.grid(row=2, column=2, padx=5, pady=5)

        tag_label = tk.Label(upper_left_frame, text="Tag:")
        tag_label.grid(row=3, column=0, padx=5, pady=5)
        self.tag_label = tk.Label(upper_left_frame, text="tag_name")
        self.tag_label.grid(row=3, column=1, padx=5, pady=5)

        # Lower Left Section
        lower_left_frame = tk.Frame(self)
        lower_left_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=2)

        # Create a canvas widget to contain the image and add scrollbars
        self.canvas = tk.Canvas(lower_left_frame, width=600, height=500,
                                bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar_x = tk.Scrollbar(lower_left_frame, orient="horizontal",
                                        command=self.canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.scrollbar_y = tk.Scrollbar(lower_left_frame, orient="vertical",
                                        command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.canvas.configure(xscrollcommand=self.scrollbar_x.set,
                              yscrollcommand=self.scrollbar_y.set)

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Upper Right Section
        upper_right_frame = tk.Frame(self)
        upper_right_frame.grid(
                row=0, column=1, padx=10, pady=10, sticky="nsew"
        )
        self.grid_columnconfigure(1, weight=1)

        comment_entry_label = tk.Label(
                upper_right_frame, text="Enter Comment:"
        )
        comment_entry_label.pack()
        self.comment_entry = tk.Text(upper_right_frame, height=10, width=50)
        self.comment_entry.pack()
        comment_button = tk.Button(
                upper_right_frame, text="Comment", command=self.comment
        )
        comment_button.pack()

        # Lower Right Section
        lower_right_frame = tk.Frame(self)
        lower_right_frame.grid(
                row=1, column=1, padx=10, pady=10, sticky="nsew"
        )

        self.comments_table = ttk.Treeview(lower_right_frame, columns=(
            "Username", "Time Taken", "Comment"), show="headings")
        self.comments_table.heading("Username", text="Username")
        self.comments_table.heading("Time Taken", text="Time Taken")
        self.comments_table.heading("Comment", text="Comment")
        self.comments_table.column("Username", width=65)
        self.comments_table.column("Time Taken", width=125)
        self.comments_table.column("Comment", width=400)
        self.comments_table.pack(side="left", fill="both", expand=True)

        scrollbar_y = ttk.Scrollbar(lower_right_frame, orient="vertical",
                                    command=self.comments_table.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.comments_table.configure(yscrollcommand=scrollbar_y.set)

        self.resizable(False, False)

        if self.screenshot_id:
            self.find_photo(self.screenshot_id)

    @staticmethod
    def validate_numeric_input(new_value):
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False

    def find_photo(self, photo_id=None):
        if not photo_id:
            photo_id = int(self.photo_id_entry.get())

        photo, time_taken, tag, comments = find_photo_by_id(photo_id)
        if photo:
            self.screenshot_id = photo_id
            self.update_selected_photo(photo, time_taken, tag, comments)
        else:
            messagebox.showerror("Error", "Photo not found")

    def browse_screenshot(self):
        screenshot_browser = ScreenshotBrowser(self)
        screenshot_browser.mainloop()

    def update_selected_photo(self, photo, time_taken, tag, comments):
        screenshot_photo = Image.open(io.BytesIO(photo))
        self.screenshot_photo = ImageTk.PhotoImage(screenshot_photo)
        self.canvas.delete("image")

        self.canvas.create_image(0, 0, anchor="nw",
                                 image=self.screenshot_photo, tags="image")
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.photo_id_entry.delete(0, tk.END)
        self.selected_photo_label.config(text=self.screenshot_id)
        self.time_taken_label.config(text=time_taken)
        self.tag_label.config(text=tag)

        self.comments_table.delete(*self.comments_table.get_children())
        for comment in comments:
            self.comments_table.insert("", "end", values=comment)

    def comment(self):
        comment_text = self.comment_entry.get("1.0", tk.END).strip()
        if comment_text:
            upload_comment(comment_text, self.user_id, self.screenshot_id)
            messagebox.showinfo("Success", "Comment uploaded successfully")
            self.destroy()
        else:
            messagebox.showerror("Error", "Please enter a comment")
