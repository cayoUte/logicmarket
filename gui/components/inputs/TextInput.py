import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from gui.theme.app_pallete import get_app_color
from gui.theme.inputs import get_input_theme
from gui.theme.fonts import get_font

def TextField(parent, placeholder="", width=200, variant="primary", bg_parent=None, ui_mode="light", label=None):
    """
    Input de texto estilo MD3 renderizado con Pillow.
    Soporta bordes redondeados y modo oscuro.
    """
    
    # 1. Obtener Tema Dinámico
    theme = get_input_theme(variant, mode=ui_mode)
    
    def resolve(v):
        return get_app_color(v[0], v[1]) if isinstance(v, (tuple, list)) else v

    # Resolver colores
    colors = {
        "bg_idle": resolve(theme["bg_idle"]),
        "bg_focus": resolve(theme["bg_focus"]),
        "border_idle": resolve(theme["border_idle"]),
        "border_focus": resolve(theme["border_focus"]),
        "text": resolve(theme["text_color"]),
        "placeholder": resolve(theme["placeholder"]),
        "cursor": resolve(theme["cursor"]),
        "parent_bg": bg_parent if bg_parent else resolve(("neutral", 0)) # Fallback seguro
    }
    
    # Si no pasaron bg_parent, intentamos leerlo del widget padre
    if not bg_parent:
        try: colors["parent_bg"] = parent.cget("bg")
        except: pass

    height = theme["height"]
    radius = theme["radius"]

    # 2. Estructura Principal
    # Si hay label, usamos un Frame contenedor, si no, devolvemos el Canvas directo
    if label:
        container = tk.Frame(parent, bg=colors["parent_bg"])
        lbl = tk.Label(container, text=label, bg=colors["parent_bg"], fg=colors["text"], font=get_font("caption"))
        lbl.pack(anchor="w", pady=(0, 4))
    else:
        container = None # No container needed logic later

    # 3. Canvas del Input
    # Este será el widget principal si no hay label
    target_parent = container if container else parent
    
    canvas = tk.Canvas(
        target_parent, 
        width=width, 
        height=height, 
        bg=colors["parent_bg"], 
        highlightthickness=0, 
        cursor="xterm"
    )
    if container: canvas.pack()

    # 4. Estado Interno
    state = {
        "focused": False,
        "is_placeholder": True if placeholder else False,
        "image_cache": {}
    }

    # 5. Motor de Renderizado (Draw)
    def draw():
        canvas.delete("bg_shape")
        
        # Determinar colores actuales
        is_focus = state["focused"]
        current_bg = colors["bg_focus"] if is_focus else colors["bg_idle"]
        current_border = colors["border_focus"] if is_focus else colors["border_idle"]
        border_width = 2 if is_focus else 1 # Borde más grueso al enfocar

        cache_key = (width, height, radius, current_bg, current_border, border_width, colors["parent_bg"])
        
        if cache_key not in state["image_cache"]:
            scale = 4
            W, H, R = width * scale, height * scale, radius * scale
            
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_ctx = ImageDraw.Draw(img)
            
            # Dibujar rectángulo redondeado con borde
            draw_ctx.rounded_rectangle(
                (0, 0, W-1, H-1), 
                radius=R, 
                fill=current_bg, 
                outline=current_border, 
                width=border_width * scale
            )
            
            # Resize y Blending
            final_img = img.resize((width, height), Image.LANCZOS)
            bg_layer = Image.new("RGBA", (width, height), colors["parent_bg"])
            bg_layer.paste(final_img, (0, 0), final_img)
            
            state["image_cache"][cache_key] = ImageTk.PhotoImage(bg_layer)
        
        tk_img = state["image_cache"][cache_key]
        canvas.create_image(width/2, height/2, image=tk_img, tags="bg_shape")
        canvas.image_ref = tk_img 
        canvas.tag_lower("bg_shape")
        
        # Actualizar color del Entry (si cambia el fondo al enfocar)
        entry.config(bg=current_bg)

    # 6. Widget Entry Nativo
    # Flota dentro del canvas
    entry = tk.Entry(
        canvas,
        bd=0,
        font=get_font("body"),
        highlightthickness=0,
        relief="flat",
        bg=colors["bg_idle"], # Inicial
        fg=colors["placeholder"], # Inicial
        insertbackground=colors["cursor"] # Color del cursor
    )
    
    # Padding horizontal (x=10)
    canvas.create_window(10, height/2, window=entry, width=width-20, height=height-8, anchor="w")

    # 7. Lógica de Placeholder y Eventos
    def on_focus_in(e):
        state["focused"] = True
        if state["is_placeholder"]:
            entry.delete(0, "end")
            entry.config(fg=colors["text"])
            state["is_placeholder"] = False
        draw()

    def on_focus_out(e):
        state["focused"] = False
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=colors["placeholder"])
            state["is_placeholder"] = True
        draw()

    # Init
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=colors["placeholder"])
    else:
        state["is_placeholder"] = False
        entry.config(fg=colors["text"])

    draw() # Primer pintado

    # Bindings
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    canvas.bind("<Button-1>", lambda e: entry.focus_set())

    # 8. Métodos Públicos
    def get_value():
        if state["is_placeholder"]: return ""
        return entry.get()

    def set_value(text):
        entry.delete(0, "end")
        if text:
            entry.insert(0, text)
            entry.config(fg=colors["text"])
            state["is_placeholder"] = False
        else:
            on_focus_out(None) # Restaurar placeholder

    # Exponer métodos en el widget contenedor (Container si hay label, Canvas si no)
    main_widget = container if container else canvas
    
    main_widget.get_value = get_value
    main_widget.set_value = set_value
    main_widget.entry_widget = entry # Acceso directo por si acaso
    
    # Método grid/pack proxy si usamos container
    if container:
        # Si devolvemos un Frame contenedor, aseguramos que grid/pack funcionen sobre él
        pass 

    return main_widget