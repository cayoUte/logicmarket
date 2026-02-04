import tkinter as tk
from gui.theme.app_pallete import get_app_color
from gui.theme.buttons import get_icon_theme
import gui.utils as utils

def IconButton(parent, icon_path, on_click, size=24, bg_parent=None, variant="primary", is_selected=False, ui_mode="light"):
    theme = get_icon_theme(variant, mode=ui_mode) # <--- USAR LA FUNCIÓN
    
    def resolve(v):
        return get_app_color(v[0], v[1]) if isinstance(v, (tuple, list)) else v

    # Resolvemos el fondo real (del padre o del tema)
    real_bg_parent = bg_parent if bg_parent else resolve(theme["parent_bg"])
    
    state = {
        "hover": False, 
        "pressed": False, 
        "selected": is_selected, # Estado inicial
        "bg_parent": real_bg_parent,
        "color_normal": resolve(theme["normal"]),
        "color_hover": resolve(theme["hover_icon"]),
        "bg_hover": resolve(theme["hover_bg"]),
        "color_active": resolve(theme["active"]),
        "image_cache": {}
    }

    padding = 8
    c_size = size + (padding * 2)
    
    canvas = tk.Canvas(
        parent, 
        width=c_size, 
        height=c_size, 
        bg=real_bg_parent, 
        highlightthickness=0, 
        cursor="hand2"
    )

    def draw(offset=0):
        canvas.delete("all")
        
        # Determinar si está activo (Hover o Seleccionado permanentemente)
        active = state["hover"] or state["selected"]
        
        # Determinar colores según estado
        if state["pressed"]:
            icon_color = state["color_active"]
            bg_circle = state["bg_hover"]
            center_offset = 1
        elif active:
            icon_color = state["color_hover"]
            bg_circle = state["bg_hover"]
            center_offset = 0
        else:
            icon_color = state["color_normal"]
            bg_circle = real_bg_parent
            center_offset = 0

        center = (c_size / 2) + center_offset

        # 1. Dibujar Círculo de Fondo (Solo si está activo/presionado)
        if active or state["pressed"]:
            # Usamos get_circle_image para bordes suaves sobre el fondo del padre
            img = utils.get_circle_image(c_size - 2, bg_circle, real_bg_parent)
            canvas.create_image(center, center, image=img)
            canvas.circle_ref = img # Retener referencia

        # 2. Dibujar Icono SVG
        # Importante: El 'bg' del icono debe ser el del círculo (si hay) o el del padre
        icon_bg_context = bg_circle 
        
        tk_icon = utils.load_svg_icon(
            f"gui/assets/icons/{icon_path}", 
            size, 
            icon_color, 
            icon_bg_context
        )
        
        if tk_icon:
            canvas.create_image(center, center, image=tk_icon)
            canvas.icon_ref = tk_icon

    # Dibujado inicial
    draw()

    # --- EXPONER MÉTODOS PÚBLICOS (FIX CRÍTICO) ---
    def set_selected(val):
        state["selected"] = val
        draw()
        
    canvas.set_selected = set_selected

    # --- Eventos ---
    canvas.bind("<Enter>", lambda e: [state.update({"hover": True}), draw()])
    canvas.bind("<Leave>", lambda e: [state.update({"hover": False, "pressed": False}), draw()])
    canvas.bind("<Button-1>", lambda e: [state.update({"pressed": True}), draw()])
    
    def on_release(e):
        state.update({"pressed": False})
        draw()
        if on_click and 0 <= e.x <= c_size and 0 <= e.y <= c_size:
            on_click()
            
    canvas.bind("<ButtonRelease-1>", on_release)

    return canvas