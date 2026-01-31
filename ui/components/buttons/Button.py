import ui.styles as styles
import ui.utils as utils
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

def Pillow_Button(parent, text, on_click, hooks, width=150, height=45, radius=20, **initial_props):
    props = utils.props_to_obj(initial_props)
    
    # 1. state INTERNO
    state = {
        "pressed": False,
        "hover": False,
        "color_actual": props.primary,
        "color_hover": getattr(props, "primary_hover", props.primary),
        "color_active": getattr(props, "primary_active", props.primary),
        "bg_parent": props.bg_app,
        "text_color": props.text_btn, # Agregamos esto al state
        "image_cache": {} 
    }

    # 2. CANVAS
    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg=state["bg_parent"],
        highlightthickness=0,
        cursor="hand2"
    )

    # --- FUNCIÓN HELPER PARA GENERAR IMAGEN SUAVIZADA ---
    def crear_imagen_redondeada(w, h, r, color_fg, color_bg):
        """Genera una imagen PIL con bordes redondeados suavizados."""
        # Creamos una imagen 4 veces más grande para el super-sampling (antialiasing)
        scale = 4
        W, H, R = w * scale, h * scale, r * scale
        
        # Imagen base transparente
        image = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Dibujamos el rectángulo redondeado en alta resolución
        # Usamos el color de fondo del padre como "color de borde" para integrarlo
        draw.rounded_rectangle((0, 0, W-1, H-1), R, fill=color_fg, outline=color_bg, width=scale)
        
        # Reducimos la imagen al tamaño original con suavizado LISIO (LANZCOS)
        image = image.resize((w, h), Image.LANCZOS)
        return ImageTk.PhotoImage(image)


    # 3. LÓGICA DE DIBUJADO ACTUALIZADA
    def dibujar(offset=0):
        canvas.delete("all")
        
        # Determinar color
        if state["pressed"]: color = state["color_active"]
        elif state["hover"]: color = state["color_hover"]
        else: color = state["color_actual"]

        # Crear clave única para el caché
        cache_key = (color, state["bg_parent"], width, height, radius)

        # Obtener o generar imagen
        if cache_key not in state["image_cache"]:
            state["image_cache"][cache_key] = crear_imagen_redondeada(
                width, height, radius, color, state["bg_parent"]
            )
        
        tk_image = state["image_cache"][cache_key]
        
        # Colocar la imagen en el centro del Canvas
        canvas.create_image(width/2 + offset, height/2 + offset, image=tk_image)

        # Texto Centrado (encima de la imagen)
        canvas.create_text(
            width/2 + offset, 
            height/2 + offset, 
            text=text, 
            fill=props.text_btn, 
            font=props.font_btn
        )
        # Necesario para mantener la referencia a la imagen y que no se borre
        canvas.image = tk_image 

    # Dibujo inicial
    dibujar()

    # --- 4. EVENTOS (Sin cambios importantes) ---
    def on_enter(e):
        state["hover"] = True
        if not state["pressed"]: dibujar(offset=0)

    def on_leave(e):
        state["hover"] = False
        state["pressed"] = False
        dibujar(offset=0)

    def on_press(e):
        state["pressed"] = True
        dibujar(offset=2) # Efecto de hundimiento

    def on_release(e):
        if state["pressed"]:
            state["pressed"] = False
            dibujar(offset=0)
            if 0 <= e.x <= width and 0 <= e.y <= height:
                if on_click: on_click()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)

    # --- 5. REACTIVIDAD (HOOKS) ACTUALIZADA ---
    # Creamos una función de actualización que pueda ser llamada externamente
    def update_style(new_props_dict):
        p = utils.props_to_obj(new_props_dict)
        
        # Actualizamos todo el state interno con los nuevos props
        state["bg_parent"] = p.bg_app
        state["color_actual"] = p.primary
        state["color_hover"] = getattr(p, "primary_hover", p.primary)
        state["color_active"] = getattr(p, "primary_active", p.primary)
        state["text_color"] = p.text_btn
        
        # Limpiamos caché porque los colores cambiaron
        state["image_cache"] = {} 
        
        # Actualizamos fondo y redibujamos
        canvas.configure(bg=p.bg_app)
        dibujar()

    # El hook global usa esta misma función
    hooks['subscribe'](canvas, lambda w, p: update_style(p))

    # --- CAMBIO FINAL IMPORTANTE ---
    # Devolvemos el widget Y la función para controlarlo
    return canvas, update_style