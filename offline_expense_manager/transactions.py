from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

from file_handler import load_transactions, save_transactions
from utils import DATE_FORMAT, CATEGORIES, TYPES


class TransactionStore:
    def __init__(self) -> None:
        self._transactions: List[Dict[str, Any]] = load_transactions()

    @property
    def transactions(self) -> List[Dict[str, Any]]:
        return list(self._transactions)

    def _persist(self) -> None:
        save_transactions(self._transactions)

    def add(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        item = dict(transaction)
        item.setdefault("id", str(uuid4()))
        self._transactions.append(item)
        self._persist()
        return item

    def update(self, transaction_id: str, updates: Dict[str, Any]) -> bool:
        for idx, item in enumerate(self._transactions):
            if item.get("id") == transaction_id:
                updated = dict(item)
                updated.update(updates)
                updated["id"] = transaction_id
                self._transactions[idx] = updated
                self._persist()
                return True
        return False

    def delete(self, transaction_id: str) -> bool:
        for idx, item in enumerate(self._transactions):
            if item.get("id") == transaction_id:
                del self._transactions[idx]
                self._persist()
                return True
        return False

    def sort(self, key: str, reverse: bool = False) -> List[Dict[str, Any]]:
        return sorted(self._transactions, key=lambda item: self._sort_key(item, key), reverse=reverse)

    def sort_items(self, items: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
        return sorted(items, key=lambda item: self._sort_key(item, key), reverse=reverse)

    def _sort_key(self, item: Dict[str, Any], key: str) -> Any:
        if key == "date":
            try:
                return datetime.strptime(item.get("date", ""), DATE_FORMAT)
            except ValueError:
                return datetime.min
        if key == "amount":
            return float(item.get("amount", 0))
        if key == "category":
            return item.get("category", "")
        return item.get(key, "")

    def filter(self, *, date_from: Optional[str] = None, date_to: Optional[str] = None,
               category: Optional[str] = None, ttype: Optional[str] = None,
               notes_query: Optional[str] = None) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for item in self._transactions:
            if date_from and not self._date_in_range(item, date_from, None):
                continue
            if date_to and not self._date_in_range(item, None, date_to):
                continue
            if category and category in CATEGORIES and item.get("category") != category:
                continue
            if ttype and ttype in TYPES and item.get("type") != ttype:
                continue
            if notes_query:
                notes = str(item.get("notes", "")).lower()
                if notes_query.lower() not in notes:
                    continue
            results.append(item)
        return results

    def _date_in_range(self, item: Dict[str, Any], date_from: Optional[str], date_to: Optional[str]) -> bool:
        try:
            value = datetime.strptime(item.get("date", ""), DATE_FORMAT)
        except ValueError:
            return False
        if date_from:
            try:
                start = datetime.strptime(date_from, DATE_FORMAT)
            except ValueError:
                return False
            if value < start:
                return False
        if date_to:
            try:
                end = datetime.strptime(date_to, DATE_FORMAT)
            except ValueError:
                return False
            if value > end:
                return False
        return True

    def summary(self) -> Dict[str, Any]:
        total_income = 0.0
        total_expense = 0.0
        category_totals = {category: 0.0 for category in CATEGORIES}
        for item in self._transactions:
            amount = float(item.get("amount", 0))
            if item.get("type") == "Income":
                total_income += amount
            else:
                total_expense += amount
                category = item.get("category")
                if category in category_totals:
                    category_totals[category] += amount
        balance = total_income - total_expense
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "category_totals": category_totals,
        }
