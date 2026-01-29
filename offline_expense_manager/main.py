import tkinter as tk
from tkinter import ttk

from gui import ExpenseManagerApp


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    ExpenseManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
