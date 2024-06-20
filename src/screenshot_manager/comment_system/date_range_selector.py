import tkinter as tk
from tkcalendar import Calendar


class DateRangeSelector(tk.Toplevel):
    def __init__(self, date_range_label):
        super().__init__(date_range_label)
        self.title("Select Date Range")

        self.date_range_label = date_range_label

        # Left Frame for Start Date
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", padx=10, pady=10)

        start_label = tk.Label(self.left_frame, text="Start Date")
        start_label.pack(side="top")

        self.start_calendar = Calendar(
                self.left_frame, selectmode="day", date_pattern="yyyy-mm-dd"
        )
        self.start_calendar.pack(side="bottom")

        # Right Frame for End Date
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", padx=10, pady=10)

        end_label = tk.Label(self.right_frame, text="End Date")
        end_label.pack(side="top")

        self.end_calendar = Calendar(
                self.right_frame, selectmode="day", date_pattern="yyyy-mm-dd"
        )
        self.end_calendar.pack(side="bottom")

        # Bottom Frame for Confirm Button
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side="bottom", pady=10)

        self.confirm_button = tk.Button(
                self.bottom_frame,
                text="Confirm",
                command=self.confirm_selection
        )
        self.confirm_button.pack()

        self.start_date = None
        self.end_date = None

    def confirm_selection(self):
        self.start_date = self.start_calendar.get_date()
        self.end_date = self.end_calendar.get_date()
        self.date_range_label.config(
            text=f"Selected Date Range: {self.start_date} to {self.end_date}")
        self.destroy()
