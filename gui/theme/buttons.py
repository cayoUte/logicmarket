# gui/theme/buttons.py
from gui.theme.app_pallete import APP_PALETTE

def get_button_theme(variant, mode="light"):
    """
    Genera la configuración del botón dinámicamente según el modo.
    mode: 'light' | 'dark'
    """
    variant = variant if variant in APP_PALETTE else "primary"
    
    # 1. Definimos colores base según el modo
    if mode == "dark":
        default_parent_bg = ("dark", "Basic") # Fondo oscuro del AppBar/Page
        default_text = ("neutral", 0)         # Texto blanco
        surface_bg = ("dark", 700)            # Color para botones tipo 'surface'
    else:
        default_parent_bg = ("neutral", 0)    # Fondo blanco
        default_text = ("neutral", 0)         # Texto blanco (para botones solidos)
        surface_bg = ("neutral", 0)

    # 2. Configuración Base (Primary, Error, Success, etc.)
    # Los botones sólidos (filled) suelen mantener su color, 
    # pero su fondo de recorte (parent_bg) debe coincidir con el tema.
    theme = {
        "main": (variant, "Basic"),
        "hover": (variant, 600),
        "active": (variant, 800),
        "text": ("neutral", 0), # Texto blanco en botones sólidos
        "parent_bg": default_parent_bg, 
        "border": None
    }

    # 3. Overrides específicos (Casos especiales)
    
    # Caso A: Botón "Surface" o "Neutral" (Ej: Botones de paginación o filtros)
    # En Light: Fondo blanco, Texto negro.
    # En Dark: Fondo gris oscuro, Texto blanco.
    if variant == "surface" or variant == "neutral":
        if mode == "dark":
            theme.update({
                "main": surface_bg,        # Gris oscuro
                "hover": ("dark", 600),
                "active": ("dark", 500),
                "text": ("neutral", 0),    # Texto Blanco
                "parent_bg": default_parent_bg,
                "border": ("dark", 500)
            })
        else:
            theme.update({
                "main": ("neutral", 0),    # Blanco
                "hover": ("neutral", 50),
                "active": ("neutral", 100),
                "text": ("neutral", 900),  # Texto Negro
                "parent_bg": ("neutral", 0),
                "border": ("neutral", 200)
            })

    # Caso B: Botón Dark (Si lo usas explícitamente)
    elif variant == "dark":
        theme.update({
            "main": ("primary", 900),
            "hover": ("primary", 800),
            "text": ("neutral", 0),
            "parent_bg": default_parent_bg
        })

    return theme

# --- ICON THEMES ---

def get_icon_theme(variant, mode="light"):
    """
    Genera configuración de iconos dinámica.
    """
    if mode == "dark":
        default_parent_bg = ("dark", "Basic")
        normal_icon_color = ("neutral", 200) # Gris claro
        hover_bg = ("dark", 600)             # Círculo hover oscuro
    else:
        default_parent_bg = ("neutral", 0)
        normal_icon_color = ("neutral", 400) # Gris medio
        hover_bg = (variant, 150) if variant != "neutral" else ("neutral", 100)

    theme = {
        "normal": normal_icon_color,
        "hover_icon": (variant, "Basic"), # El icono se colorea al hover
        "hover_bg": hover_bg,             # El círculo de fondo
        "active": (variant, 900),
        "parent_bg": default_parent_bg,
    }
    
    # Override para neutral en light mode
    if variant == "neutral" and mode == "light":
        theme["hover_icon"] = ("primary", "Basic")
        theme["hover_bg"] = ("secondary", "Basic")

    return theme