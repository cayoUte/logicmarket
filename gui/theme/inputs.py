from gui.theme.app_pallete import APP_PALETTE

def get_input_theme(variant, mode="light"):
    """
    Genera la configuración del input dinámicamente.
    """
    # 1. Definir colores base según el modo
    if mode == "dark":
        # Dark Mode: Inputs oscuros con borde sutil
        bg_idle = ("dark", 800)        # Fondo muy oscuro
        bg_focus = ("dark", 800)       # Mismo fondo al enfocar
        border_idle = ("dark", 500)    # Borde grisáceo
        text_color = ("neutral", 50)   # Texto casi blanco
        placeholder = ("neutral", 400) # Texto gris medio
        cursor = ("neutral", 0)        # Cursor blanco
    else:
        # Light Mode: Inputs claros/blancos
        bg_idle = ("neutral", 0)       # Fondo blanco
        bg_focus = ("neutral", 0)
        border_idle = ("neutral", 200) # Borde gris claro
        text_color = ("neutral", 900)  # Texto negro
        placeholder = ("neutral", 400)
        cursor = ("neutral", 900)      # Cursor negro

    # 2. El color de borde al enfocar depende de la variante (primary, error, etc)
    if variant in APP_PALETTE:
        border_focus = (variant, "Basic")
    else:
        border_focus = ("primary", "Basic")

    return {
        "bg_idle": bg_idle,
        "bg_focus": bg_focus,
        "border_idle": border_idle,
        "border_focus": border_focus,
        "text_color": text_color,
        "placeholder": placeholder,
        "cursor": cursor,
        "height": 40, # Altura estándar un poco más cómoda
        "radius": 8   # Radio de borde sutil (no tan redondo como los botones)
    }
    
def get_textfield_theme(mode="light"):
    """
    Configuración específica para 'Filled Text Fields' (Material Design).
    Define colores para reposo, foco y error en ambos modos.
    """
    if mode == "dark":
        # --- DARK MODE ---
        return {
            "bg_idle": ("dark", 700),          # Gris oscuro (Surface Container Highest)
            "bg_hover": ("dark", 600),         # Un poco más claro al pasar el mouse
            
            "indicator_idle": ("neutral", 500),# Línea inferior gris
            "indicator_focus": ("primary", "Basic"), # Línea activa (Color marca)
            "indicator_error": ("error", "Basic"),
            
            "label_idle": ("neutral", 300),    # Etiqueta gris claro
            "label_focus": ("primary", "Basic"),
            "label_error": ("error", "Basic"),
            
            "text": ("neutral", 50),           # Texto escrito (Blanco/Hueso)
            "caret": ("primary", "Basic"),     # Cursor
            
            "supporting": ("neutral", 400),    # Texto de ayuda
            "supporting_error": ("error", "Basic")
        }
    else:
        # --- LIGHT MODE (Tu configuración original) ---
        return {
            "bg_idle": ("neutral", 25),
            "bg_hover": ("neutral", 50),
            
            "indicator_idle": ("neutral", 400),
            "indicator_focus": ("primary", "Basic"),
            "indicator_error": ("error", "Basic"),
            
            "label_idle": ("neutral", 400),
            "label_focus": ("primary", "Basic"),
            "label_error": ("error", "Basic"),
            
            "text": ("neutral", 900),
            "caret": ("primary", "Basic"),
            
            "supporting": ("neutral", 400),
            "supporting_error": ("error", "Basic")
        }