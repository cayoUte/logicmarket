FONTS = {
    "family": ("Roboto", "Segoe UI", "Helvetica", "Arial", "sans-serif"),
    "weight_normal": "normal",
    "weight_bold": "bold",
    "size_sm": 10,
    "size_md": 12,
    "size_lg": 14,
    "size_xl": 18,
}

LIGHT_THEME = {
    "bg_app": "#f0f2f5",
    "bg_component": "#ffffff",
    "surface": "#ffffff",
    "border": "#e0e0e0",
    "text_main": "#1c1e21",
    "text_secondary": "#65676b",
    "text_btn": "#ffffff",
    "primary": "#6200EA",
    "primary_hover": "#7C4DFF",
    "primary_active": "#304FFE",
    "text_on_primary": "#ffffff",
    "secondary": "#0039d5",
    "secondary_hover": "#2e5bd6",
    "secondary_active": "#002a9e",
    "text_on_secondary": "#ffffff",
    "error": "#d32f2f",
    "success": "#2e7d32",
    "warning": "#ed6c02",
    "bg_sidebar": "#ffffff",
    "text_sidebar": "#546e7a",
    "sidebar_active": "#e3f2fd",
    "sidebar_active_text": "#1976d2",
    "divider": "#eceff1",
}

DARK_THEME = {
    "bg_app": "#121212",
    "bg_component": "#2d2d2d",
    "surface": "#1e1e1e",
    "border": "#444444",
    "text_main": "#e4e6eb",
    "text_secondary": "#b0b3b8",
    "text_btn": "#000000",
    "primary": "#BB86FC",
    "primary_hover": "#9965f4",
    "primary_active": "#7F39FB",
    "text_on_primary": "#000000",
    "secondary": "#4dabf5",
    "secondary_hover": "#2196f3",
    "secondary_active": "#1769aa",
    "text_on_secondary": "#000000",
    "error": "#ef5350",
    "success": "#66bb6a",
    "warning": "#ffa726",
    "bg_sidebar": "#1e1e1e",
    "text_sidebar": "#b0bec5",
    "sidebar_active": "#323232",
    "sidebar_active_text": "#90caf9",
    "divider": "#424242",
}


def get_theme(mode="light"):
    colors = LIGHT_THEME if mode == "light" else DARK_THEME

    font_family_str = (
        FONTS["family"][0] if isinstance(FONTS["family"], tuple) else FONTS["family"]
    )

    calculated_props = {
        "font_btn": (font_family_str, FONTS["size_sm"], FONTS["weight_bold"])
    }

    return {**colors, **FONTS, **calculated_props}
