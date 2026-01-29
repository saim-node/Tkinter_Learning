import tkinter as tk
from tkinter import ttk

# Create main window
window = tk.Tk()
window.title("Simple Inventory System")
window.geometry("600x400")

# Labels
tk.Label(window, text="Item Name").grid(row=0, column=0, padx=5, pady=5)
tk.Label(window, text="Quantity").grid(row=0, column=1, padx=5, pady=5)
tk.Label(window, text="Price").grid(row=0, column=2, padx=5, pady=5)

# Entry fields
nameEntry = tk.Entry(window)
qtyEntry = tk.Entry(window)
priceEntry = tk.Entry(window)

nameEntry.grid(row=1, column=0, padx=5, pady=5)
qtyEntry.grid(row=1, column=1, padx=5, pady=5)
priceEntry.grid(row=1, column=2, padx=5, pady=5)

# Treeview
columns = ("name", "qty", "price")
tree = ttk.Treeview(window, columns=columns, show="tree headings")
tree.heading("name", text="Item Name")
tree.heading("qty", text="Quantity")
tree.heading("price", text="Price")
tree.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")



window.mainloop()
