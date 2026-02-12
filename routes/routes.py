
from gui.pages.HomePage import HomePage
from gui.pages.InventoryPage import InventoryPage
from gui.pages.ImporterPage import ImporterPage
routes = {
        "home": HomePage,
        "inventory": InventoryPage,
        "importer": ImporterPage,        
    }

menu_items = [
        {"id": "home", "icon": "home.svg"},
        {"id": "importer", "icon": "security.svg"},
        {"id": "inventory", "icon": "inventory.svg"},        
    ]


