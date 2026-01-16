import ui.styles as styles
import ui.utils as utils
import tkinter as tk


def Button(parent, text, on_click, hooks, type="primary", **initial_props):
    defaults = styles.get_theme("light")
    props = utils.props_to_obj(initial_props, defaults)
    bg_color = getattr(props, type, props.primary)

    btn = tk.Button(
        parent,
        text=text,
        command=on_click,
        bg=bg_color,
        fg=props.text_on_primary,
        font=(props.family, props.size_md, props.weight_bold),
        padx=10,
        pady=5,
        relief="flat",
        activebackground=bg_color,
        cursor="hand2",
    )

    def update(widget, new_theme_dict):
        p = utils.props_to_obj(new_theme_dict)
        new_bg = getattr(p, type)
        widget.configure(bg=new_bg, fg=p.text_on_primary, activebackground=new_bg)

    hooks["subscribe"](btn, update)
    
    return btn

def Styled_Button(parent, text, on_click, hooks, width=150, height=45, radius=20, **initial_props):
    props = utils.props_to_obj(initial_props)
    
    # --- 1. ESTADO INTERNO (CLAUSURA) ---
    # Al no usar clases, usamos un diccionario mutable para guardar el estado
    state = {
        "pressed": False,
        "hover": False,
        # Guardamos los colores actuales para no perderlos
        "current_color": props.primary, 
        "color_hover": getattr(props, "primary_hover", props.primary),
        "color_active": getattr(props, "primary_active", props.primary)
    }

    # --- 2. CONFIGURACIÓN DEL CANVAS ---
    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=props.bg_app,      # ¡CRUCIAL! Esto hace que las esquinas sean transparentes
        highlightthickness=0, # Quita el borde feo por defecto
        cursor="hand2"
    )

    # --- 3. LÓGICA DE DIBUJADO (Tu algoritmo original adaptado) ---
    def render(offset=0):
        canvas.delete("all")
        
        # Determinar color según estado
        if state["pressed"]:
            color = state["color_active"]
        elif state["hover"]:
            color = state["color_hover"]
        else:
            color = state["current_color"]

        # Coordenadas
        x1, y1 = offset, offset
        x2, y2 = width - offset, height - offset # Ajuste para que no se corte
        r = radius

        # Formas Geométricas
        # Esquinas
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=color, outline=color)
        
        # Rellenos
        canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=color, outline=color)
        canvas.create_rectangle(x1, y1+r, x2, y2-r, fill=color, outline=color)

        # Texto Centrado
        canvas.create_text(
            width/2 + offset, 
            height/2 + offset, 
            text=text, 
            fill=props.text_btn, 
            font=props.font_btn
        )

    # Dibujo inicial
    render()

    # --- 4. EVENTOS (INTERACTIVIDAD) ---
    def on_enter(e):
        state["hover"] = True
        if not state["pressed"]:
            render(offset=0)

    def on_leave(e):
        state["hover"] = False
        state["pressed"] = False # Resetear por seguridad
        render(offset=0)

    def on_press(e):
        state["pressed"] = True
        render(offset=2) # Efecto de hundimiento

    def on_release(e):
        if state["pressed"]:
            state["pressed"] = False
            render(offset=0)
            # Ejecutar comando solo si soltó dentro del botón
            if 0 <= e.x <= width and 0 <= e.y <= height:
                if on_click: on_click()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)

    # --- 5. REACTIVIDAD (HOOKS) ---
    def update_theme(widget, new_props_dict):
        p = utils.props_to_obj(new_props_dict)
        
        # 1. Actualizar fondo del canvas para que coincida con la app
        widget.configure(bg=p.bg_app)
        
        # 2. Actualizar colores internos del estado
        state["current_color"] = p.primary
        state["color_hover"] = getattr(p, "primary_hover", p.primary)
        state["color_active"] = getattr(p, "primary_active", p.primary)
        
        # 3. Redibujar
        render()

    hooks['subscribe'](canvas, update_theme)

    return canvas