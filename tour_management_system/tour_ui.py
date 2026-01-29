import tkinter as tk
from tkinter import messagebox

from models import Tour, tours


def tour_window() -> None:
    win = tk.Toplevel()
    win.title("Tours")
    win.geometry("420x460")

    def refresh_list() -> None:
        listbox.delete(0, tk.END)
        for tour in tours:
            listbox.insert(tk.END, f"{tour.tour_id} | {tour.destination} | ${tour.price:.2f} | {tour.duration} days | {tour.seats} seats")

    def clear_form() -> None:
        tid.delete(0, tk.END)
        dest.delete(0, tk.END)
        price.delete(0, tk.END)
        duration.delete(0, tk.END)
        seats.delete(0, tk.END)

    def add_tour() -> None:
        if not tid.get().strip() or not dest.get().strip():
            messagebox.showerror("Error", "Tour ID and Destination are required.", parent=win)
            return
        try:
            tour = Tour(tid.get().strip(), dest.get().strip(), price.get().strip(), duration.get().strip(), seats.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Price, Duration, and Seats must be numbers.", parent=win)
            return
        if any(t.tour_id == tour.tour_id for t in tours):
            messagebox.showerror("Error", "Tour ID already exists.", parent=win)
            return
        tours.append(tour)
        refresh_list()
        clear_form()

    def update_tour() -> None:
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Select", "Select a tour to update.", parent=win)
            return
        index = selection[0]
        try:
            updated = Tour(tid.get().strip(), dest.get().strip(), price.get().strip(), duration.get().strip(), seats.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Price, Duration, and Seats must be numbers.", parent=win)
            return
        tours[index] = updated
        refresh_list()

    def delete_tour() -> None:
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Select", "Select a tour to delete.", parent=win)
            return
        if not messagebox.askyesno("Confirm", "Delete selected tour?", parent=win):
            return
        tours.pop(selection[0])
        refresh_list()
        clear_form()

    def load_selected(_event=None) -> None:
        selection = listbox.curselection()
        if not selection:
            return
        tour = tours[selection[0]]
        clear_form()
        tid.insert(0, tour.tour_id)
        dest.insert(0, tour.destination)
        price.insert(0, str(tour.price))
        duration.insert(0, str(tour.duration))
        seats.insert(0, str(tour.seats))

    tk.Label(win, text="Tour ID").pack()
    tid = tk.Entry(win)
    tid.pack()

    tk.Label(win, text="Destination").pack()
    dest = tk.Entry(win)
    dest.pack()

    tk.Label(win, text="Price").pack()
    price = tk.Entry(win)
    price.pack()

    tk.Label(win, text="Duration (days)").pack()
    duration = tk.Entry(win)
    duration.pack()

    tk.Label(win, text="Available Seats").pack()
    seats = tk.Entry(win)
    seats.pack()

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Add Tour", command=add_tour).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Update Tour", command=update_tour).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Delete Tour", command=delete_tour).grid(row=0, column=2, padx=5)

    listbox = tk.Listbox(win, height=8, width=55)
    listbox.pack(pady=10)
    listbox.bind("<<ListboxSelect>>", load_selected)

    refresh_list()
