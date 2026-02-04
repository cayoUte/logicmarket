
import io
import re
import resvg_py
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageTk, ImageDraw
from PIL import ImageOps

_icon_cache = {}


def get_circle_image(size, color, bg_parent):
    cache_key = f"circle_{size}_{color}_{bg_parent}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    scale = 4
    d = size * scale

    img = Image.new("RGBA", (d, d), bg_parent)
    draw = ImageDraw.Draw(img)

    draw.ellipse((0, 0, d, d), fill=color)

    img = img.resize((size, size), Image.Resampling.LANCZOS)

    tk_img = ImageTk.PhotoImage(img)
    _icon_cache[cache_key] = tk_img
    return tk_img


def load_svg_icon(path, size, color, bg_parent):
    """
    Carga un SVG, cambia su color, lo renderiza a PNG de alta calidad 
    y lo fusiona con el fondo del padre.
    """
    # 1. Clave de caché (incluye bg_parent para diferenciar temas)
    cache_key = f"{path}_{size}_{color}_{bg_parent}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    try:
        # 2. Leer archivo
        with open(path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # 3. Reemplazar colores (Tu lógica de Regex original)
        def color_replacer(match):
            tag_content = match.group(0)
            if 'fill="none"' in tag_content: return tag_content
            if "fill=" in tag_content:
                return re.sub(r'fill="[^"]+"', f'fill="{color}"', tag_content)
            else:
                return tag_content.replace("<path", f'<path fill="{color}"')

        svg_content = re.sub(r"<path[^>]*>", color_replacer, svg_content)

        if "fill=" not in svg_content and "<svg" in svg_content:
            svg_content = svg_content.replace("<svg", f'<svg fill="{color}"')

        # 4. RENDERIZADO (CORRECCIÓN AQUÍ)
        # resvg_py.svg_to_bytes convierte el string SVG directamente a bytes PNG
        png_data = resvg_py.svg_to_bytes(svg_content)

        # 5. Cargar en Pillow
        # Como png_data ya es un archivo PNG válido en memoria, usamos Image.open
        pil_image = Image.open(io.BytesIO(png_data)).convert("RGBA")

        # 6. Redimensionar (LANCZOS para calidad máxima)
        # resvg renderiza al tamaño original del SVG, así que redimensionamos aquí
        if pil_image.size != (size, size):
             pil_image = pil_image.resize((size, size), Image.Resampling.LANCZOS)

        # 7. FUSION DE FONDO (Técnica Anti-Halo)
        # Creamos un fondo sólido del color del padre (bg_parent)
        background = Image.new("RGBA", (size, size), bg_parent)
        
        # Pegamos el icono encima. Los bordes transparentes se mezclarán con bg_parent.
        final_image = Image.alpha_composite(background, pil_image)

        # 8. Convertir a formato Tkinter y guardar en caché
        photo_image = ImageTk.PhotoImage(final_image)
        _icon_cache[cache_key] = photo_image
        return photo_image

    except Exception as e:
        print(f"Error loading SVG {path}: {e}")
        # Retorna una imagen vacía o placeholder para que la app no crashee
        return None



def get_circle_avatar(image_path, size=(40, 40), bg_color="#FFFFFF"):
    """Retorna un objeto PhotoImage circular."""
    try:
        img = Image.open(image_path).convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        
        # Crear imagen compuesta con fondo por si hay transparencias
        bg = Image.new("RGBA", size, bg_color)
        bg.paste(output, (0, 0), output)
        return ImageTk.PhotoImage(bg)
    except Exception as e:
        print(f"Error cargando avatar: {e}")
        return None

def apply_hover_effect(widget, colors):
    """Aplica eventos de hover basados en tu diccionario ICON_THEMES."""
    # colors espera: {'normal': ..., 'hover_icon': ..., 'hover_bg': ...}
    def on_enter(e):
        widget.config(bg=colors['hover_bg'][1] if isinstance(colors['hover_bg'], tuple) else colors['hover_bg'])
        # Si fuera un label con texto/icono, cambiarías fg aquí
        
    def on_leave(e):
        widget.config(bg=colors['parent_bg'][1] if isinstance(colors['parent_bg'], tuple) else colors['parent_bg'])

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)