import tkinter as tk
from tkinter import messagebox, ttk

from models import Booking, bookings, tours, customers, find_tour, find_customer


def booking_window() -> None:
    win = tk.Toplevel()
    win.title("Bookings")
    win.geometry("460x440")

    def refresh_dropdowns() -> None:
        tour_ids = [tour.tour_id for tour in tours]
        customer_ids = [customer.customer_id for customer in customers]
        tour_box["values"] = tour_ids
        customer_box["values"] = customer_ids

    def refresh_list() -> None:
        listbox.delete(0, tk.END)
        for booking in bookings:
            listbox.insert(tk.END, f"{booking.customer.customer_id} -> {booking.tour.tour_id} ({booking.tour.destination})")

    def book_tour() -> None:
        customer_id = customer_var.get().strip()
        tour_id = tour_var.get().strip()
        if not customer_id or not tour_id:
            messagebox.showerror("Error", "Select both customer and tour.", parent=win)
            return
        customer = find_customer(customer_id)
        tour = find_tour(tour_id)
        if not customer or not tour:
            messagebox.showerror("Error", "Invalid customer or tour.", parent=win)
            return
        if tour.seats <= 0:
            messagebox.showerror("Error", "No seats available.", parent=win)
            return
        tour.seats -= 1
        bookings.append(Booking(customer, tour))
        refresh_list()

    tk.Label(win, text="Customer ID").pack(pady=(10, 0))
    customer_var = tk.StringVar()
    customer_box = ttk.Combobox(win, textvariable=customer_var, state="readonly")
    customer_box.pack()

    tk.Label(win, text="Tour ID").pack(pady=(10, 0))
    tour_var = tk.StringVar()
    tour_box = ttk.Combobox(win, textvariable=tour_var, state="readonly")
    tour_box.pack()

    tk.Button(win, text="Book Tour", command=book_tour).pack(pady=10)

    listbox = tk.Listbox(win, height=10, width=50)
    listbox.pack(pady=10)

    refresh_dropdowns()
    refresh_list()
