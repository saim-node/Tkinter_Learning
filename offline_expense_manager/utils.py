from __future__ import annotations

from datetime import datetime
from typing import Tuple

DATE_FORMAT = "%Y-%m-%d"
CATEGORIES = ["Food", "Transport", "Entertainment", "Bills", "Others"]
TYPES = ["Income", "Expense"]


def today_str() -> str:
    return datetime.today().strftime(DATE_FORMAT)


def parse_date(value: str) -> Tuple[bool, str]:
    value = (value or "").strip()
    if not value:
        return False, "Date is required."
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return False, f"Date must be in {DATE_FORMAT} format."
    return True, ""


def parse_amount(value: str) -> Tuple[bool, float, str]:
    raw = (value or "").strip()
    if not raw:
        return False, 0.0, "Amount is required."
    try:
        amount = float(raw)
    except ValueError:
        return False, 0.0, "Amount must be numeric."
    return True, amount, ""


def validate_category(value: str) -> Tuple[bool, str]:
    if value not in CATEGORIES:
        return False, "Please select a valid category."
    return True, ""


def validate_type(value: str) -> Tuple[bool, str]:
    if value not in TYPES:
        return False, "Please select a valid type."
    return True, ""


def normalize_notes(value: str) -> str:
    return (value or "").strip()
