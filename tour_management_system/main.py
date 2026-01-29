import tkinter as tk
from tkinter import messagebox

from dashboard import open_dashboard


def login() -> None:
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
