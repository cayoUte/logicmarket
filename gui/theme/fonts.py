import os
from tkextrafont import Font


def load_custom_fonts():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fonts_path = os.path.join(base_path, "assets", "fonts")

    font_files = ["Montserrat-SemiBold.ttf", "Roboto-Regular.ttf", "Roboto-Bold.ttf"]

    print(f"🔄 Cargando fuentes desde: {fonts_path}")

    for filename in font_files:
        full_path = os.path.join(fonts_path, filename)
        try:
            Font(file=full_path)

        except Exception as e:
            if "already loaded" in str(e):
                pass
            else:
                print(f"   Error {filename}: {e}")

    print("✅ Sistema de fuentes listo.")


FAMILIES = {
    "brand": ("Montserrat SemiBold", "Montserrat", "Arial"),
    "ui": ("Segoe UI", "Helvetica", "Arial"),
    "data": ("Roboto", "Arial", "Consolas"),
}


STYLES = {
    "h1": {"family": FAMILIES["brand"], "size": 48, "weight": "normal"},
    "h2": {"family": FAMILIES["brand"], "size": 32, "weight": "normal"},
    "h3": {"family": FAMILIES["brand"], "size": 24, "weight": "normal"},
    "h4": {"family": FAMILIES["brand"], "size": 18, "weight": "normal"},
    "h5": {"family": FAMILIES["brand"], "size": 14, "weight": "normal"},
    "h6": {"family": FAMILIES["brand"], "size": 12, "weight": "normal"},
    "body": {"family": FAMILIES["ui"], "size": 12, "weight": "normal"},
    "body_bold": {"family": FAMILIES["ui"], "size": 12, "weight": "bold"},
    "button": {"family": FAMILIES["ui"], "size": 12, "weight": "bold"},
    "input": {"family": FAMILIES["data"], "size": 10, "weight": "normal"},
    "table_header": {"family": FAMILIES["data"], "size": 10, "weight": "bold"},
    "table_row": {"family": FAMILIES["data"], "size": 10, "weight": "normal"},
}


def get_font(style_name):
    style = STYLES.get(style_name, STYLES["body"])
    return (style["family"][0], style["size"], style["weight"])


def get_font_family(style_name):
    style = STYLES.get(style_name, STYLES["body"])
    return style["family"][0]
