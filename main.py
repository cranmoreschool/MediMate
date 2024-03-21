import tkinter as tk
from tkcalendar import Calendar
import datetime
import pygame.mixer

class MedicineReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediMate Reminder")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Select the date and time for your medicine reminder:", font=("Helvetica", 12))
        self.label.pack(pady=10)

        # Calendar widget
        self.cal = Calendar(root, selectmode="day", date_pattern="dd-mm-yyyy")
        self.cal.pack(pady=10)

        # Time selection (unchanged)
        self.time_label = tk.Label(root, text="Select the time:")
        self.time_label.pack()
        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.hour_entry = tk.Entry(root, textvariable=self.hour_var, width=2)
        self.hour_entry.pack(side=tk.LEFT)
        self.colon_label = tk.Label(root, text=":")
        self.colon_label.pack(side=tk.LEFT)
        self.minute_entry = tk.Entry(root, textvariable=self.minute_var, width=2)
        self.minute_entry.pack(side=tk.LEFT)

        # Day selection for recurring reminder (unchanged)
        self.recur_label = tk.Label(root, text="Select the day for recurring reminder:")
        self.recur_label.pack()
        self.day_var = tk.StringVar()
        self.day_var.set("Monday")
        self.day_option_menu = tk.OptionMenu(root, self.day_var, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        self.day_option_menu.pack(pady=5)

        # Button to set reminder (unchanged)
        self.set_button = tk.Button(root, text="Set Reminder", command=self.set_reminder)
        self.set_button.pack(pady=10)

        # Button for testing reminder (unchanged)
        self.test_button = tk.Button(root, text="TEST Reminder", command=self.test_reminder)
        self.test_button.pack(pady=5)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

    def set_reminder(self):
        selected_date = self.cal.get_date()
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        day_of_week = self.day_var.get()

        reminder_datetime = datetime.datetime.strptime(selected_date, "%d-%m-%Y").replace(hour=hour, minute=minute)

        # Adjust reminder date to the next occurrence of the selected day of the week
        while reminder_datetime.strftime('%A') != day_of_week:
            reminder_datetime += datetime.timedelta(days=1)

        now = datetime.datetime.now()
        time_diff = reminder_datetime - now

        if time_diff.total_seconds() < 0:
            # If the selected date has already passed, add a week to the reminder
            reminder_datetime += datetime.timedelta(weeks=1)

        # Calculate the time until the next reminder
        time_diff = reminder_datetime - now

        # Schedule the reminder using tkinter's after method
        self.root.after(int(time_diff.total_seconds() * 1000), self.show_reminder)

    def show_reminder(self):
        self.play_sound()
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("Reminder")
        reminder_window.geometry("300x100")
        reminder_label = tk.Label(reminder_window, text="It's time to take your medicine!", font=("Helvetica", 12))
        reminder_label.pack(pady=20)
        dismiss_button = tk.Button(reminder_window, text="Dismiss", command=reminder_window.destroy)
        dismiss_button.pack()

    def test_reminder(self):
        self.set_reminder()

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("beep.wav")
        pygame.mixer.music.play()

def main():
    root = tk.Tk()
    app = MedicineReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
