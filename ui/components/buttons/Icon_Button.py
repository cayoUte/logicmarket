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
        "bg_parent": props.bg_app,
        # Default colors (Icon takes the 'text_main' color usually, or primary)
        "color_normal": props.bg_app, 
        "color_hover": props.primary,
        "color_active": props.primary_active
    }

    # 2. CANVAS SETUP
    # We use a square canvas + padding
    padding = 8
    canvas_size = size + (padding * 2)
    print( f"Creating IconButton with size {canvas_size} (icon size {size} + padding {padding*2}) + bg {state['bg_parent']}" )
    canvas = tk.Canvas(
        parent,
        width=canvas_size,
        height=canvas_size,
        bg='#000000',
        highlightthickness=0,
        cursor="hand2"
    )

    # 3. DRAWING LOGIC
    def draw():
        canvas.delete("all")
        
        # Determine Color
        if state["pressed"]:
            current_color = state["color_active"]
            bg_fill = props.sidebar_active # Optional: Background circle on click
        elif state["hover"]:
            current_color = state["color_hover"]
            bg_fill = props.bg_app # Or a subtle hover color
        else:
            current_color = state["color_normal"]
            bg_fill = state["bg_parent"]

        # Determine Offset (Click effect)
        offset = 1 if state["pressed"] else 0

        # Optional: Draw Hover Background Circle/Rounded Rect
        if state["hover"]:
             # Draw a circle with a contrasting color for the hover effect
             canvas.create_oval(
                 2, 2, canvas_size-2, canvas_size-2, 
                 fill=bg_fill, # Use a contrasting color from styles
                 outline=""
                 
             )
        # Load and Draw Icon
        # We assume the icon is at assets/icons/
        full_path = f"ui/assets/material_icons/{icon_path}" 
        
        tk_icon = utils.load_svg_icon(full_path, size, current_color)
        
        if tk_icon:
            canvas.create_image(
                canvas_size/2 + offset, 
                canvas_size/2 + offset, 
                image=tk_icon, 
                anchor="center",                                
            )
            canvas.image = tk_icon
            canvas.configure(bg=state["bg_parent"])
        else:
            # Fallback visual si falla svglib (ej. un círculo de color)
            r = size / 2
            cx, cy = canvas_size/2 + offset, canvas_size/2 + offset
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=current_color)
            # Keep reference to avoid garbage collection
            canvas.image = tk_icon

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
        
        widget.configure(bg=p.bg_app)
        draw()

    hooks['subscribe'](canvas, update_theme)

    return canvas