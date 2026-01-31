import json
import os

DB_FILE = "inventario.txt"

def load_inventory_from_file():
    """Lee el archivo de texto y devuelve una lista de diccionarios."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_inventory_to_file(inventory):
    """Escribe el estado actual en el archivo de texto."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=4, ensure_ascii=False)