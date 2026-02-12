import json
import os

DB_FILE = "inventario.txt"


def load_inventory_from_file():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_inventory_to_file(inventory):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4, ensure_ascii=False)
