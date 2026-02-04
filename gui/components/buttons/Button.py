from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from gui.theme.fonts import get_font
from gui.theme.app_pallete import get_app_color
from gui.theme.buttons import get_button_theme
import gui.utils as utils

def Pillow_Button(parent, text, on_click, icon_path=None, dimensions=(150, 45, 20), variant="primary", bg_parent=None, is_selected=False, ui_mode="light"):
    width, height, radius = dimensions
    # 1. OBTENER TEMA DINÁMICO
    theme = get_button_theme(variant, mode=ui_mode) # <--- USAR LA FUNCIÓN
    font_config = get_font("button")

    def resolve_color(value):
        if value is None: return None
        if isinstance(value, (tuple, list)) and len(value) == 2:
            return get_app_color(value[0], value[1])
        return value

    real_bg_parent = bg_parent if bg_parent else resolve_color(theme["parent_bg"])

    state = {
        "pressed": False,
        "hover": False,
        "selected": is_selected, # Soporte para selección
        "current_color": resolve_color(theme["main"]),
        "hover_color": resolve_color(theme["hover"]),
        "active_color": resolve_color(theme["active"]),
        "text_color": resolve_color(theme["text"]),
        "border_color": resolve_color(theme["border"]),
        "image_cache": {},
    }

    canvas = tk.Canvas(parent, width=width, height=height, bg=real_bg_parent, highlightthickness=0, cursor="hand2")

    def draw(offset=0):
        canvas.delete("all")
        
        # Lógica de color: Selected actúa como Hover persistente o Active
        is_active = state["hover"] or state["selected"]
        
        if state["pressed"]:
             fill_col = state["active_color"]
        elif is_active:
             fill_col = state["hover_color"]
        else:
             fill_col = state["current_color"]
             
        outline_col = state["border_color"] if state["border_color"] else real_bg_parent

        cache_key = (fill_col, outline_col, width, height, radius, real_bg_parent)
        
        if cache_key not in state["image_cache"]:
            scale = 4
            W, H, R = width * scale, height * scale, radius * scale
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_ctx = ImageDraw.Draw(img)
            stroke = 4 if state["border_color"] else 0
            
            draw_ctx.rounded_rectangle((0, 0, W - 1, H - 1), R, fill=fill_col, outline=outline_col, width=stroke)
            
            final_img = img.resize((width, height), Image.LANCZOS)
            bg_layer = Image.new("RGBA", (width, height), real_bg_parent)
            bg_layer.paste(final_img, (0, 0), final_img)
            state["image_cache"][cache_key] = ImageTk.PhotoImage(bg_layer)

        tk_bg = state["image_cache"][cache_key]
        canvas.create_image(width / 2 + offset, height / 2 + offset, image=tk_bg)

        # Contenido (Texto/Icono)
        content_y = height / 2 + offset
        icon_color = state["text_color"]
        
        if icon_path:
            icon_size = 18
            tk_icon = utils.load_svg_icon(f"gui/assets/icons/{icon_path}", icon_size, icon_color, fill_col)
            
            gap = 8
            text_width = len(text) * 7
            total_w = icon_size + gap + text_width
            start_x = (width - total_w) / 2 + (icon_size / 2)
            
            canvas.create_image(start_x - (gap / 2) - (icon_size / 2), content_y, image=tk_icon)
            canvas.create_text(start_x + gap + (text_width / 2) - (icon_size / 2), content_y, text=text, fill=icon_color, font=font_config)
            canvas.icon_ref = tk_icon
        else:
            canvas.create_text(width / 2 + offset, content_y, text=text, fill=icon_color, font=font_config)

        canvas.bg_ref = tk_bg

    draw()

    # --- EXPONER MÉTODO ---
    def set_selected(val):
        state["selected"] = val
        draw()
    canvas.set_selected = set_selected

    # Eventos
    canvas.bind("<Enter>", lambda e: [state.update({"hover": True}), draw()])
    canvas.bind("<Leave>", lambda e: [state.update({"hover": False, "pressed": False}), draw()])
    canvas.bind("<Button-1>", lambda e: [state.update({"pressed": True}), draw(2)])
    canvas.bind("<ButtonRelease-1>", lambda e: [state.update({"pressed": False}), draw(), on_click() if 0 <= e.x <= width and 0 <= e.y <= height else None])

    return canvas