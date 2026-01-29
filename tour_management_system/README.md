# Tour Management System (Tkinter | In-Memory)

## 📌 Description
This is a desktop-based Tour Management System built using Python and Tkinter.
All data is stored temporarily in memory (no files, no database).

## 🛠 Technologies
- Python 3.x
- Tkinter
- Object-Oriented Programming

## ✨ Features
- Admin login
- Tour management (CRUD)
- Customer management
- Booking system
- Seat availability validation

## ▶️ How to Run
```bash
python main.py
```

## 🔑 Login Credentials

Username: admin

Password: admin123

## ⚠️ Note

All data is lost when the application is closed.

## 🚀 Future Enhancements

File storage

Database support

Search & filters

Reports

---

## 🧱 MODELS (`models.py`)

```python
class Tour:
    def __init__(self, tour_id, destination, price, duration, seats):
        self.tour_id = tour_id
        self.destination = destination
        self.price = price
        self.duration = duration
        self.seats = seats


class Customer:
    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email


class Booking:
    def __init__(self, customer, tour):
        self.customer = customer
        self.tour = tour
```

## 🖥️ MAIN ENTRY (`main.py`) – WORKING LOGIN
```python
import tkinter as tk
from tkinter import messagebox
from dashboard import open_dashboard


def login():
    if username.get() == "admin" and password.get() == "admin123":
        root.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Login")

root = tk.Tk()
root.title("Login")
root.geometry("300x200")

tk.Label(root, text="Username").pack(pady=5)
username = tk.Entry(root)
username.pack()

tk.Label(root, text="Password").pack(pady=5)
password = tk.Entry(root, show="*")
password.pack()

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
```

## 🧭 DASHBOARD (`dashboard.py`)
```python
import tkinter as tk
from tour_ui import tour_window
from customer_ui import customer_window
from booking_ui import booking_window


def open_dashboard():
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("400x300")

    tk.Label(dash, text="Tour Management System",
             font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(dash, text="Manage Tours", width=20,
              command=tour_window).pack(pady=5)

    tk.Button(dash, text="Manage Customers", width=20,
              command=customer_window).pack(pady=5)

    tk.Button(dash, text="Bookings", width=20,
              command=booking_window).pack(pady=5)

    dash.mainloop()
```

## 🧳 TOUR UI (BASIC VERSION)
```python
import tkinter as tk
from models import Tour

tours = []


def tour_window():
    win = tk.Toplevel()
    win.title("Tours")

    def add_tour():
        tour = Tour(
            tid.get(), dest.get(),
            price.get(), duration.get(), seats.get()
        )
        tours.append(tour)
        status.config(text="Tour Added")

    tid = tk.Entry(win)
    dest = tk.Entry(win)
    price = tk.Entry(win)
    duration = tk.Entry(win)
    seats = tk.Entry(win)

    for label, widget in zip(
        ["ID", "Destination", "Price", "Duration", "Seats"],
        [tid, dest, price, duration, seats]
    ):
        tk.Label(win, text=label).pack()
        widget.pack()

    tk.Button(win, text="Add Tour", command=add_tour).pack(pady=10)
    status = tk.Label(win, text="")
    status.pack()
```

## 🔥 WHY THIS IS “ADVANCED”

Clean separation of concerns

Real application workflow

Multi-window architecture

OOP-based data models
