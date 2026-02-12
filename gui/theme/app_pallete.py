"""
app_pallete.py
Generador dinámico de paletas de colores.
"""


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*[int(c) for c in rgb])


def mix_colors(color1, color2, weight):
    return tuple(c1 * (1 - weight) + c2 * weight for c1, c2 in zip(color1, color2))


def generate_palette(base_hex):
    base_rgb = hex_to_rgb(base_hex)
    white_rgb = (255, 255, 255)
    black_rgb = (0, 0, 0)

    palette = {}
    keys = [
        0,
        25,
        50,
        75,
        100,
        150,
        200,
        300,
        400,
        "Basic",
        600,
        700,
        750,
        800,
        850,
        900,
        925,
        950,
        975,
        1000,
    ]

    for key in keys:
        if key == "Basic":
            palette["Basic"] = base_hex
            palette["main"] = base_hex
            continue

        numeric_value = key
        if numeric_value == 0:
            palette[key] = "#ffffff"
        elif numeric_value == 1000:
            palette[key] = "#000000"
        elif numeric_value < 500:
            weight = numeric_value / 500.0
            mixed_rgb = mix_colors(white_rgb, base_rgb, weight)
            palette[key] = rgb_to_hex(mixed_rgb)
        else:
            weight = (numeric_value - 500) / 500.0
            mixed_rgb = mix_colors(base_rgb, black_rgb, weight)
            palette[key] = rgb_to_hex(mixed_rgb)

    return palette


BASE_COLORS = {
    "primary": "#E8A2B3",
    "secondary": "#A2E8D7",
    "neutral": "#8b9cac",
    "warning": "#f49258",
    "error": "#da3737",
    "success": "#55da6b",
}

APP_PALETTE = {cat: generate_palette(col) for cat, col in BASE_COLORS.items()}

APP_PALETTE["surface"] = generate_palette("#ffffff")
APP_PALETTE["dark"] = generate_palette("#1e1e1e")


def get_app_color(category, shade):
    category = category.lower().strip()
    if isinstance(shade, str) and shade.lower() != "basic":
        try:
            shade = int(shade)
        except ValueError:
            pass

    try:
        return APP_PALETTE[category][shade]
    except KeyError:
        return "#ff00ff"
