import io
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageTk, ImageDraw

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
    cache_key = f"{path}_{size}_{color}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    try:
        with open(path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        def color_replacer(match):
            tag_content = match.group(0)
            if 'fill="none"' in tag_content:
                return tag_content
            if "fill=" in tag_content:
                return re.sub(r'fill="[^"]+"', f'fill="{color}"', tag_content)
            else:
                return tag_content.replace("<path", f'<path fill="{color}"')

        svg_content = re.sub(r"<path[^>]*>", color_replacer, svg_content)

        if "fill=" not in svg_content and "<svg" in svg_content:
            svg_content = svg_content.replace("<svg", f'<svg fill="{color}"')

        svg_file = io.BytesIO(svg_content.encode("utf-8"))
        drawing = svg2rlg(svg_file)

        png_data = renderPM.drawToString(drawing, fmt="PNG", bg=bg_parent)

        pil_image = Image.open(io.BytesIO(png_data))

        pil_image = pil_image.convert("RGBA")

        pil_image = pil_image.resize((size, size), Image.Resampling.LANCZOS)

        photo_image = ImageTk.PhotoImage(pil_image)
        _icon_cache[cache_key] = photo_image
        return photo_image

    except Exception as e:
        print(f"Error loading SVG {path}: {e}")
        return None
