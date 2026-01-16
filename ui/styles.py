

FONTS = {
    "family": "Roboto",
    "weight_normal": "normal",
    "weight_bold": "bold",
    "size_sm": 10,
    "size_md": 12,
    "size_lg": 14,
}

LIGHT_THEME = {
    "bg_app": "#f0f2f5",      # Un gris muy suave moderno
    "primary": "#6200EA",     # Violeta Material Design
    "primary_hover": "#7C4DFF",
    "primary_active": "#304FFE", 
    "text_btn": "#ffffff",
    "font_btn": ("Segoe UI", 10, "bold"),
    "bg_component": '#ffffff',
    "text_main": '#000000',
    "secondary": "#0039d5",
    "error": "#f4368b",
    "success": '#2e7d32',
    "warning": '#ed6c02',
    "surface": "#a00000ff",
    "border": '#e0e0e0',
    "text_on_primary": "#ffecec"
}
DARK_THEME = {
    "bg_app": "#121212",
    "primary": "#BB86FC",     # Violeta pastel para Dark Mode
    "primary_hover": "#9965f4",
    "primary_active": "#7F39FB", 
    "text_btn": "#000000",    # Texto oscuro sobre color pastel
    "font_btn": ("Segoe UI", 10, "bold"),
    "bg_component": '#2d2d2d',
    "text_main": '#ffffff',
    "secondary": "#2e5bd6",
    "error": '#ef5350',
    "success": '#66bb6a',
    "warning": '#ffa726',
    "surface": "#333333",
    "border": '#444444',
    "text_on_primary": "#000000"
}

def get_theme(mode='light'):
    colors = LIGHT_THEME if mode == 'light' else DARK_THEME
    return {**colors, **FONTS}


        