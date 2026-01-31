import tkinter as tk
from ui import utils

def IconButton(parent, icon_path, on_click, hooks, size=24, **initial_props):
    """
    A pure Icon Button (no text), useful for toolbars or compact menus.
    """
    props = utils.props_to_obj(initial_props)
    
    # 1. INTERNAL STATE
    state = {
        "hover": False,
        "pressed": False,
        "bg_parent": props.bg_app, # Este es el color que necesitamos
        "color_normal": props.text_secondary, 
        "color_hover": props.primary,
        "color_active": props.primary_active
    }

    # 2. CANVAS SETUP
    padding = 8
    canvas_size = size + (padding * 2)
    
    canvas = tk.Canvas(
        parent,
        width=canvas_size,
        height=canvas_size,
        # --- CORRECCIÓN: Usar el color del padre, NO negro fijo ---
        bg=state['bg_parent'], 
        # ---------------------------------------------------------
        highlightthickness=0,
        cursor="hand2"
    )

    # 3. DRAWING LOGIC
    def draw():
        canvas.delete("all")
        
        # Determine Color
        if state["pressed"]:
            current_color = state["color_active"]
            bg_fill = props.sidebar_active 
        elif state["hover"]:
            current_color = state["color_hover"]
            bg_fill = props.sidebar_active
        else:
            current_color = state["color_normal"]
            bg_fill = state["bg_parent"]

        offset = 1 if state["pressed"] else 0
        center = int(canvas_size / 2) + offset

        # Optional: Draw Hover Background Circle/Rounded Rect
        if state["hover"]:
            # Usamos la imagen suave de utils en lugar de create_oval pixelado
            circle_diameter = canvas_size - 2
            # Pasamos el color de relleno (violeta claro) y el color de fondo "camuflaje"
            tk_circle = utils.get_circle_image(circle_diameter, bg_fill, state["bg_parent"])
            
            canvas.create_image(
                center, center, 
                image=tk_circle, 
                anchor="center"
            )
            # Guardamos referencia para que no se borre de memoria
            canvas.bg_image = tk_circle 

        # Load and Draw Icon
        full_path = f"ui/assets/material_icons/{icon_path}"
        
        # Pasamos el color del fondo actual para el "camuflaje" del SVG
        bg_camuflaje = bg_fill if state["hover"] else state["bg_parent"]
        
        tk_icon = utils.load_svg_icon(full_path, size, current_color, bg_camuflaje)
        
        if tk_icon:
            canvas.create_image(
                center, center, 
                image=tk_icon, 
                anchor="center"
            )
            canvas.icon_image = tk_icon 
        
        # Asegurar que el fondo del canvas coincida con el padre si cambió el tema
        canvas.configure(bg=state["bg_parent"])

    draw()

    # 4. EVENTS
    def on_enter(e):
        state["hover"] = True
        draw()

    def on_leave(e):
        state["hover"] = False
        state["pressed"] = False
        draw()

    def on_press(e):
        state["pressed"] = True
        draw()

    def on_release(e):
        if state["pressed"]:
            state["pressed"] = False
            draw()
            if 0 <= e.x <= canvas_size and 0 <= e.y <= canvas_size:
                if on_click: on_click()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)

    # 5. REACTIVITY
    def update_theme(widget, new_props):
        p = utils.props_to_obj(new_props)
        state["bg_parent"] = p.bg_app
        state["color_normal"] = p.text_secondary
        state["color_hover"] = p.primary
        state["color_active"] = p.primary_active
        
        # Importante: actualizar el fondo del widget canvas
        widget.configure(bg=p.bg_app)
        draw()

    hooks['subscribe'](canvas, update_theme)

    return canvas