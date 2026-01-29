import tkinter as tk

from tour_ui import tour_window
from customer_ui import customer_window
from booking_ui import booking_window


def open_dashboard() -> None:
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("400x300")

    tk.Label(dash, text="Tour Management System", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(dash, text="Manage Tours", width=20, command=tour_window).pack(pady=5)
    tk.Button(dash, text="Manage Customers", width=20, command=customer_window).pack(pady=5)
    tk.Button(dash, text="Bookings", width=20, command=booking_window).pack(pady=5)

    dash.mainloop()
