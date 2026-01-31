
from gui.pages.HomePage import HomePage
from gui.pages.PricingPage import PricingPage
from gui.pages.Monitor import InventoryPage
from gui.pages.CRUD import ImporterPage
routes = {
        "home": HomePage,
        "inventory": InventoryPage,
        "importer": ImporterPage,
        "settings": PricingPage,
    }

menu_items = [
        {"id": "home", "icon": "home.svg"},
        {"id": "importer", "icon": "security.svg"},
        {"id": "inventory", "icon": "inventory.svg"},
        {"id": "settings", "icon": "psychology.svg"},
    ]


