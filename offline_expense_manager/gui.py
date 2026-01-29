from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any

from transactions import TransactionStore
from utils import CATEGORIES, TYPES, today_str, parse_date, parse_amount, validate_category, validate_type, normalize_notes


class ExpenseManagerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Offline Personal Expense Manager")
        self.store = TransactionStore()

        self._build_main_ui()

    def _build_main_ui(self) -> None:
        self.root.geometry("600x400")
        self.root.minsize(520, 320)

        header = ttk.Label(self.root, text="Offline Personal Expense Manager", font=("Segoe UI", 18, "bold"))
        header.pack(pady=20)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Transaction", command=self.open_add_transaction).grid(row=0, column=0, padx=8, pady=6)
        ttk.Button(button_frame, text="View Transactions", command=self.open_view_transactions).grid(row=0, column=1, padx=8, pady=6)
        ttk.Button(button_frame, text="Summary", command=self.open_summary).grid(row=0, column=2, padx=8, pady=6)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).grid(row=0, column=3, padx=8, pady=6)

        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

    def open_add_transaction(self) -> None:
        TransactionForm(self.root, self.store, on_saved=self._refresh_all)

    def open_view_transactions(self) -> None:
        TransactionsWindow(self.root, self.store, on_change=self._refresh_all)

    def open_summary(self) -> None:
        SummaryWindow(self.root, self.store)

    def _refresh_all(self) -> None:
        pass


class TransactionForm(tk.Toplevel):
    def __init__(self, master: tk.Widget, store: TransactionStore, on_saved, transaction: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(master)
        self.store = store
        self.on_saved = on_saved
        self.transaction = transaction
        self.title("Add Transaction" if not transaction else "Edit Transaction")
        self.resizable(False, False)

        self.date_var = tk.StringVar(value=transaction.get("date") if transaction else today_str())
        self.category_var = tk.StringVar(value=transaction.get("category") if transaction else CATEGORIES[0])
        self.type_var = tk.StringVar(value=transaction.get("type") if transaction else TYPES[0])
        self.amount_var = tk.StringVar(value=str(transaction.get("amount")) if transaction else "")
        self.notes_var = tk.StringVar(value=transaction.get("notes") if transaction else "")

        self._build_form()

    def _build_form(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.date_var, width=22).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(container, text="Category").grid(row=1, column=0, sticky="w")
        category_box = ttk.Combobox(container, textvariable=self.category_var, values=CATEGORIES, state="readonly", width=20)
        category_box.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(container, text="Type").grid(row=2, column=0, sticky="w")
        type_frame = ttk.Frame(container)
        type_frame.grid(row=2, column=1, sticky="w", pady=4)
        for idx, value in enumerate(TYPES):
            ttk.Radiobutton(type_frame, text=value, value=value, variable=self.type_var).grid(row=0, column=idx, padx=4)

        ttk.Label(container, text="Amount").grid(row=3, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.amount_var, width=22).grid(row=3, column=1, sticky="ew", pady=4)

        ttk.Label(container, text="Notes").grid(row=4, column=0, sticky="nw")
        notes_entry = ttk.Entry(container, textvariable=self.notes_var)
        notes_entry.grid(row=4, column=1, sticky="ew", pady=4)

        button_frame = ttk.Frame(container)
        button_frame.grid(row=5, column=0, columnspan=2, pady=12)
        ttk.Button(button_frame, text="Save", command=self._save).grid(row=0, column=0, padx=6)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).grid(row=0, column=1, padx=6)

        container.columnconfigure(1, weight=1)

    def _save(self) -> None:
        date_value = self.date_var.get().strip()
        category = self.category_var.get()
        ttype = self.type_var.get()
        amount_value = self.amount_var.get().strip()
        notes = normalize_notes(self.notes_var.get())

        ok, message = parse_date(date_value)
        if not ok:
            messagebox.showerror("Validation Error", message, parent=self)
            return
        ok, message = validate_category(category)
        if not ok:
            messagebox.showerror("Validation Error", message, parent=self)
            return
        ok, message = validate_type(ttype)
        if not ok:
            messagebox.showerror("Validation Error", message, parent=self)
            return
        ok, amount, message = parse_amount(amount_value)
        if not ok:
            messagebox.showerror("Validation Error", message, parent=self)
            return

        payload = {
            "date": date_value,
            "category": category,
            "type": ttype,
            "amount": amount,
            "notes": notes,
        }

        if self.transaction:
            self.store.update(self.transaction["id"], payload)
        else:
            self.store.add(payload)

        if callable(self.on_saved):
            self.on_saved()
        self.destroy()


class TransactionsWindow(tk.Toplevel):
    def __init__(self, master: tk.Widget, store: TransactionStore, on_change) -> None:
        super().__init__(master)
        self.store = store
        self.on_change = on_change
        self.title("Transactions")
        self.geometry("820x520")
        self.minsize(760, 420)

        self.date_from_var = tk.StringVar()
        self.date_to_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All")
        self.type_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()
        self.sort_var = tk.StringVar(value="date")
        self.sort_dir_var = tk.StringVar(value="desc")

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        filter_frame = ttk.LabelFrame(self, text="Search & Filter", padding=10)
        filter_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        for i in range(10):
            filter_frame.columnconfigure(i, weight=1)

        ttk.Label(filter_frame, text="Date From").grid(row=0, column=0, sticky="w")
        ttk.Entry(filter_frame, textvariable=self.date_from_var, width=12).grid(row=0, column=1, sticky="ew")

        ttk.Label(filter_frame, text="Date To").grid(row=0, column=2, sticky="w", padx=(8, 0))
        ttk.Entry(filter_frame, textvariable=self.date_to_var, width=12).grid(row=0, column=3, sticky="ew")

        ttk.Label(filter_frame, text="Category").grid(row=0, column=4, sticky="w", padx=(8, 0))
        category_box = ttk.Combobox(filter_frame, textvariable=self.category_var, values=["All"] + CATEGORIES, state="readonly", width=12)
        category_box.grid(row=0, column=5, sticky="ew")

        ttk.Label(filter_frame, text="Type").grid(row=0, column=6, sticky="w", padx=(8, 0))
        type_box = ttk.Combobox(filter_frame, textvariable=self.type_var, values=["All"] + TYPES, state="readonly", width=12)
        type_box.grid(row=0, column=7, sticky="ew")

        ttk.Label(filter_frame, text="Search Notes").grid(row=1, column=0, sticky="w", pady=(6, 0))
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.grid(row=1, column=1, columnspan=3, sticky="ew", pady=(6, 0))

        ttk.Label(filter_frame, text="Sort By").grid(row=1, column=4, sticky="w", padx=(8, 0), pady=(6, 0))
        sort_box = ttk.Combobox(filter_frame, textvariable=self.sort_var, values=["date", "amount", "category"], state="readonly", width=10)
        sort_box.grid(row=1, column=5, sticky="ew", pady=(6, 0))

        sort_dir_box = ttk.Combobox(filter_frame, textvariable=self.sort_dir_var, values=["asc", "desc"], state="readonly", width=8)
        sort_dir_box.grid(row=1, column=7, sticky="ew", pady=(6, 0))

        ttk.Button(filter_frame, text="Apply", command=self.refresh).grid(row=1, column=8, padx=(8, 0), pady=(6, 0))
        ttk.Button(filter_frame, text="Clear", command=self._clear_filters).grid(row=1, column=9, padx=(8, 0), pady=(6, 0))

        self.status_label = ttk.Label(filter_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=10, sticky="w", pady=(6, 0))

        category_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        type_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        sort_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        sort_dir_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        search_entry.bind("<KeyRelease>", lambda _event: self.refresh())

        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ("date", "category", "type", "amount", "notes")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("notes", text="Notes")

        self.tree.column("date", width=100, anchor="center")
        self.tree.column("category", width=120, anchor="center")
        self.tree.column("type", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("notes", width=280, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=10)
        ttk.Button(button_frame, text="Edit Selected", command=self._edit_selected).grid(row=0, column=0, padx=6)
        ttk.Button(button_frame, text="Delete Selected", command=self._delete_selected).grid(row=0, column=1, padx=6)

    def _clear_filters(self) -> None:
        self.date_from_var.set("")
        self.date_to_var.set("")
        self.category_var.set("All")
        self.type_var.set("All")
        self.search_var.set("")
        self.sort_var.set("date")
        self.sort_dir_var.set("desc")
        self.refresh()

    def _safe_date(self, value: str) -> Optional[str]:
        value = value.strip()
        if not value:
            return None
        ok, _ = parse_date(value)
        return value if ok else None

    def refresh(self) -> None:
        self.status_label.config(text="")
        date_from = self._safe_date(self.date_from_var.get())
        date_to = self._safe_date(self.date_to_var.get())
        if self.date_from_var.get().strip() and not date_from:
            self.status_label.config(text="Invalid Date From format. Use YYYY-MM-DD.")
        if self.date_to_var.get().strip() and not date_to:
            self.status_label.config(text="Invalid Date To format. Use YYYY-MM-DD.")

        category = self.category_var.get()
        ttype = self.type_var.get()
        category_filter = None if category == "All" else category
        type_filter = None if ttype == "All" else ttype
        notes_query = self.search_var.get().strip()

        items = self.store.filter(
            date_from=date_from,
            date_to=date_to,
            category=category_filter,
            ttype=type_filter,
            notes_query=notes_query or None,
        )

        sort_key = self.sort_var.get()
        reverse = self.sort_dir_var.get() == "desc"
        items = self.store.sort_items(items, sort_key, reverse=reverse)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in items:
            self.tree.insert(
                "",
                tk.END,
                iid=item.get("id"),
                values=(
                    item.get("date"),
                    item.get("category"),
                    item.get("type"),
                    f"{float(item.get('amount', 0)):.2f}",
                    item.get("notes", ""),
                ),
            )

    def _get_selected(self) -> Optional[Dict[str, Any]]:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Transaction", "Please select a transaction.", parent=self)
            return None
        transaction_id = selected[0]
        for item in self.store.transactions:
            if item.get("id") == transaction_id:
                return item
        return None

    def _edit_selected(self) -> None:
        item = self._get_selected()
        if not item:
            return
        TransactionForm(self, self.store, on_saved=self._handle_change, transaction=item)

    def _delete_selected(self) -> None:
        item = self._get_selected()
        if not item:
            return
        if not messagebox.askyesno("Confirm Delete", "Delete the selected transaction?", parent=self):
            return
        self.store.delete(item["id"])
        self._handle_change()

    def _handle_change(self) -> None:
        if callable(self.on_change):
            self.on_change()
        self.refresh()


class SummaryWindow(tk.Toplevel):
    def __init__(self, master: tk.Widget, store: TransactionStore) -> None:
        super().__init__(master)
        self.store = store
        self.title("Summary")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        summary = self.store.summary()
        total_income = summary["total_income"]
        total_expense = summary["total_expense"]
        balance = summary["balance"]

        ttk.Label(container, text="Totals", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(container, text="Total Income:").grid(row=1, column=0, sticky="w")
        ttk.Label(container, text=f"{total_income:.2f}").grid(row=1, column=1, sticky="e")

        ttk.Label(container, text="Total Expenses:").grid(row=2, column=0, sticky="w")
        ttk.Label(container, text=f"{total_expense:.2f}").grid(row=2, column=1, sticky="e")

        ttk.Label(container, text="Current Balance:").grid(row=3, column=0, sticky="w")
        ttk.Label(container, text=f"{balance:.2f}").grid(row=3, column=1, sticky="e")

        ttk.Separator(container).grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(container, text="Category Totals", font=("Segoe UI", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=(0, 6))

        row = 6
        for category, amount in summary["category_totals"].items():
            ttk.Label(container, text=f"{category}:").grid(row=row, column=0, sticky="w")
            ttk.Label(container, text=f"{amount:.2f}").grid(row=row, column=1, sticky="e")
            row += 1

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
