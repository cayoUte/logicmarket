from gui.theme.app_pallete import get_app_color

def get_menu_theme(mode="light"):
    if mode == "dark":
        return {
            "bg": ("dark", 750),           # Surface Container
            "text": ("neutral", 50),       # On Surface
            "text_disabled": ("neutral", 500),
            "icon": ("neutral", 200),
            "hover": ("dark", 600),        # State Layer
            "divider": ("dark", 600),
            "shadow": "#000000"
        }
    else:
        return {
            "bg": ("neutral", 0),          # Surface Container Low/Lowest
            "text": ("neutral", 900),
            "text_disabled": ("neutral", 400),
            "icon": ("neutral", 500),
            "hover": ("neutral", 50),
            "divider": ("neutral", 100),
            "shadow": "#000000"
        }

MENU_SPECS = {
    "width": 200,          # Ancho estándar
    "item_height": 48,     # MD3 Spec
    "padding_vertical": 8,
    "radius": 4            # MD3 Spec (4dp para menús simples)
}