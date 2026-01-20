# styles.py

# 1. Tipografía
# Usamos una tupla para la familia: Si no encuentra Roboto, intenta Segoe UI, luego Arial.
FONTS = {
    "family": ("Roboto", "Segoe UI", "Helvetica", "Arial", "sans-serif"),
    "weight_normal": "normal",
    "weight_bold": "bold",
    "size_sm": 10,
    "size_md": 12,
    "size_lg": 14,
    "size_xl": 18, # Agregado para títulos grandes
}

# 2. Tema Claro (Light Mode)
LIGHT_THEME = {
    # --- BASES ---
    "bg_app": "#f0f2f5",       # Gris muy suave (Fondo de ventana)
    "bg_component": "#ffffff", # Fondo de inputs
    "surface": "#ffffff",      # Fondo de tarjetas/tablas (CORREGIDO: antes era rojo)
    "border": "#e0e0e0",       # Bordes sutiles
    
    # --- TEXTO ---
    "text_main": "#1c1e21",    # Gris casi negro (mejor lectura que negro puro)
    "text_secondary": "#65676b", # Para subtítulos
    "text_btn": "#ffffff",     # Texto en botones primarios
    
    # --- PRIMARIO (Violeta) ---
    "primary": "#6200EA",
    "primary_hover": "#7C4DFF",
    "primary_active": "#304FFE",
    "text_on_primary": "#ffffff",

    # --- SECUNDARIO (Azul) ---
    # Agregamos variantes para que los botones secundarios tengan animación
    "secondary": "#0039d5",
    "secondary_hover": "#2e5bd6",
    "secondary_active": "#002a9e",
    "text_on_secondary": "#ffffff",

    # --- ESTADOS ---
    "error": "#d32f2f",
    "success": "#2e7d32",
    "warning": "#ed6c02",
    
    # --- DRAWER ---
    "bg_sidebar": "#ffffff",       # Blanco puro para el sidebar
    "text_sidebar": "#546e7a",     # Gris azulado para items inactivos
    "sidebar_active": "#e3f2fd",   # Fondo azul muy claro para item activo
    "sidebar_active_text": "#1976d2", # Azul fuerte para texto activo
    "divider": "#eceff1",          # Línea separadora
}

# 3. Tema Oscuro (Dark Mode)
DARK_THEME = {
    # --- BASES ---
    "bg_app": "#121212",       # Casi negro
    "bg_component": "#2d2d2d", # Gris oscuro para inputs
    "surface": "#1e1e1e",      # Ligeramente más claro que el fondo (Elevación 1)
    "border": "#444444",       # Bordes más oscuros
    
    # --- TEXTO ---
    "text_main": "#e4e6eb",    # Blanco suave (no quema la vista)
    "text_secondary": "#b0b3b8",
    "text_btn": "#000000",     # Texto negro en botones pastel se lee mejor
    
    # --- PRIMARIO (Violeta Pastel) ---
    "primary": "#BB86FC",
    "primary_hover": "#9965f4",
    "primary_active": "#7F39FB",
    "text_on_primary": "#000000", 

    # --- SECUNDARIO (Azul Claro) ---
    "secondary": "#4dabf5",    
    "secondary_hover": "#2196f3",
    "secondary_active": "#1769aa",
    "text_on_secondary": "#000000",

    # --- ESTADOS ---
    "error": "#ef5350",
    "success": "#66bb6a",
    "warning": "#ffa726",

    #--- DRAWER ---
    "bg_sidebar": "#2d2d2d",       # Blanco puro para el sidebar
    "text_sidebar": "#546e7a",     # Gris azulado para items inactivos
    "sidebar_active": "#e3f2fd",   # Fondo azul muy claro para item activo
    "sidebar_active_text": "#1976d2", # Azul fuerte para texto activo
    "divider": "#eceff1",          # Línea separadora
}

def get_theme(mode='light'):
    colors = LIGHT_THEME if mode == 'light' else DARK_THEME
    
    # Generamos la fuente del botón dinámicamente para respetar la familia global
    # (Tomamos el primer elemento de la tupla de familias)
    font_family_str = FONTS["family"][0] if isinstance(FONTS["family"], tuple) else FONTS["family"]
    
    calculated_props = {
        "font_btn": (font_family_str, FONTS["size_sm"], FONTS["weight_bold"])
    }
    
    return {**colors, **FONTS, **calculated_props}