from __future__ import annotations

import json
import os
from typing import List, Dict, Any


def get_data_file_path() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "transactions.json")


def load_transactions() -> List[Dict[str, Any]]:
    path = get_data_file_path()
    if not os.path.exists(path):
        save_transactions([])
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, OSError):
        return []
    return []


def save_transactions(transactions: List[Dict[str, Any]]) -> None:
    path = get_data_file_path()
    with open(path, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=2)
