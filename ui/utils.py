from types import SimpleNamespace
import io
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from reportlab.lib import colors  # Importante para colors.transparent
from PIL import Image, ImageTk

# Cache to avoid parsing XML and rendering on every hover event
_icon_cache = {}

def load_svg_icon(path, size, color):
    """
    Cross-platform SVG loader using svglib with transparency support.
    Saves the rendered icon with a transparent background.
    """
    # Create a unique key for the cache
    cache_key = f"{path}_{size}_{color}"

    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    try:
        # 1. Read SVG as plain text
        with open(path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # 2. DYNAMIC COLOR REPLACEMENT (Regex Magic)
        def color_replacer(match):
            tag_content = match.group(0)
            # If fill="none" is explicitly stated, don't override it (it's transparency)
            if 'fill="none"' in tag_content:
                return tag_content
            # If a fill color exists, replace it
            if 'fill=' in tag_content:
                return re.sub(r'fill="[^"]+"', f'fill="{color}"', tag_content)
            # If no fill exists, inject it
            else:
                return tag_content.replace('<path', f'<path fill="{color}"')

        # Apply replacement to all path tags
        svg_content = re.sub(r'<path[^>]*>', color_replacer, svg_content)

        # Also handle standard <svg fill="..."> if exists
        if 'fill=' not in svg_content and '<svg' in svg_content:
             svg_content = svg_content.replace('<svg', f'<svg fill="{color}" fill-opacity="0"')

        # 3. CONVERT TO MEMORY FILE
        svg_file = io.BytesIO(svg_content.encode('utf-8'))

        # 4. RENDER TO DRAWING (ReportLab)
        drawing = svg2rlg(svg_file)

        # --- CORRECCIÓN ---
        # Eliminamos la línea 'drawing.background = ...' que causaba el error.
        # La transparencia se maneja exclusivamente en el paso de renderizado.
        # ------------------

        # 5. CONVERT TO PIL IMAGE
        # Pasamos bg=colors.transparent aquí. Esto le dice al renderizador
        # que inicie el lienzo como transparente (RGBA).
        drawing._renderPM_bg = colors.toColor('white').clone(alpha=0)

        pil_image = renderPM.drawToPIL(drawing, bg=colors.toColor('white').clone(alpha=0))  # Transparente

        # 6. RESIZE HIGH QUALITY
        pil_image = pil_image.resize((size, size), Image.Resampling.LANCZOS)

        # 7. SAVE PIL IMAGE WITH TRANSPARENT BACKGROUND
        pil_image.save("temp_icon.png", "PNG") # Save as PNG to preserve transparency

        # 8. CONVERT TO TKINTER (Optional - Remove if not needed)
        photo_image = ImageTk.PhotoImage(pil_image)

        # Save to cache
        _icon_cache[cache_key] = photo_image
        return photo_image

    except Exception as e:
        print(f"Error loading SVG {path}: {e}")
        return None


def props_to_obj(props_dict, defaults={}):
    merged = {**defaults, **props_dict}
    return SimpleNamespace(**merged)