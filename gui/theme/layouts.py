# gui/theme/layouts.py
from gui.theme.app_pallete import get_app_color

def get_drawer_theme(mode="light"):
    """
    Configuración de colores para el Sidebar/Drawer.
    """
    if mode == "dark":
        return {
            "bg": ("dark", "Basic"),       # Fondo oscuro (ej: #1E1E1E)
            "border": ("dark", 600),       # Borde sutil gris oscuro
            # Variante de iconos para el modo oscuro (normalmente primary o secondary)
            "icon_variant": "secondary"    
        }
    else:
        return {
            "bg": ("neutral", 0),          # Fondo blanco
            "border": ("neutral", 200),    # Borde gris claro
            "icon_variant": "secondary"    # Variante de color para selección
        }