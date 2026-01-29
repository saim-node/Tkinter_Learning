import tkinter as tk
from tkinter import messagebox

from models import Customer, customers


def customer_window() -> None:
    win = tk.Toplevel()
    win.title("Customers")
    win.geometry("420x420")

    def refresh_list() -> None:
        listbox.delete(0, tk.END)
        for customer in customers:
            listbox.insert(tk.END, f"{customer.customer_id} | {customer.name} | {customer.phone} | {customer.email}")

    def clear_form() -> None:
        cid.delete(0, tk.END)
        name.delete(0, tk.END)
        phone.delete(0, tk.END)
        email.delete(0, tk.END)

    def add_customer() -> None:
        if not cid.get().strip() or not name.get().strip():
            messagebox.showerror("Error", "Customer ID and Name are required.", parent=win)
            return
        if any(c.customer_id == cid.get().strip() for c in customers):
            messagebox.showerror("Error", "Customer ID already exists.", parent=win)
            return
        customer = Customer(cid.get().strip(), name.get().strip(), phone.get().strip(), email.get().strip())
        customers.append(customer)
        refresh_list()
        clear_form()

    def delete_customer() -> None:
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Select", "Select a customer to delete.", parent=win)
            return
        if not messagebox.askyesno("Confirm", "Delete selected customer?", parent=win):
            return
        customers.pop(selection[0])
        refresh_list()
        clear_form()

    def load_selected(_event=None) -> None:
        selection = listbox.curselection()
        if not selection:
            return
        customer = customers[selection[0]]
        clear_form()
        cid.insert(0, customer.customer_id)
        name.insert(0, customer.name)
        phone.insert(0, customer.phone)
        email.insert(0, customer.email)

    tk.Label(win, text="Customer ID").pack()
    cid = tk.Entry(win)
    cid.pack()

    tk.Label(win, text="Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Phone").pack()
    phone = tk.Entry(win)
    phone.pack()

    tk.Label(win, text="Email").pack()
    email = tk.Entry(win)
    email.pack()

    button_frame = tk.Frame(win)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Add Customer", command=add_customer).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Delete Customer", command=delete_customer).grid(row=0, column=1, padx=5)

    listbox = tk.Listbox(win, height=8, width=55)
    listbox.pack(pady=10)
    listbox.bind("<<ListboxSelect>>", load_selected)

    refresh_list()
