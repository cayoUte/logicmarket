# gui/theme/dialogs.py

def get_dialog_theme(mode="light"):
    if mode == "dark":
        return {
            "bg": ("dark", 750),           # Surface Container High (Gris oscuro elevado)
            "title": ("neutral", 50),      # Blanco
            "body": ("neutral", 200),      # Gris claro
            "card_bg": ("dark", 700),      # Fondo de la tarjeta interna
            "overlay": "#000000"           # Color para oscurecer el fondo (si implementas overlay manual)
        }
    else:
        return {
            "bg": ("neutral", 0),          # Blanco (Surface)
            "title": ("neutral", 900),     # Negro
            "body": ("neutral", 700),      # Gris oscuro
            "card_bg": ("neutral", 25),    # Gris muy claro
            "overlay": "#000000"
        }

DIALOG_SPECS = {
    "padding_outer": 24,
    "padding_title": 16,
    "padding_actions": 24,
    "gap_actions": 8,
    "radius": 28,
    "min_width": 320,
    "max_width": 560
}