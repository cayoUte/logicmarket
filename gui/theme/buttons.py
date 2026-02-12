# gui/theme/buttons.py
from gui.theme.app_pallete import APP_PALETTE


def get_button_theme(variant, mode="light"):
    variant = variant if variant in APP_PALETTE else "primary"

    if mode == "dark":
        default_parent_bg = ("dark", "Basic")
        surface_bg = ("dark", 700)
    else:
        default_parent_bg = ("neutral", 0)
        surface_bg = ("neutral", 0)

    theme = {
        "main": (variant, "Basic"),
        "hover": (variant, 600),
        "active": (variant, 800),
        "text": ("neutral", 0),
        "parent_bg": default_parent_bg,
        "border": None,
    }

    if variant == "surface" or variant == "neutral":
        if mode == "dark":
            theme.update(
                {
                    "main": surface_bg,
                    "hover": ("dark", 600),
                    "active": ("dark", 500),
                    "text": ("neutral", 0),
                    "parent_bg": default_parent_bg,
                    "border": ("dark", 500),
                }
            )
        else:
            theme.update(
                {
                    "main": ("neutral", 0),
                    "hover": ("neutral", 50),
                    "active": ("neutral", 100),
                    "text": ("neutral", 900),
                    "parent_bg": ("neutral", 0),
                    "border": ("neutral", 200),
                }
            )

    elif variant == "dark":
        theme.update(
            {
                "main": ("primary", 900),
                "hover": ("primary", 800),
                "text": ("neutral", 0),
                "parent_bg": default_parent_bg,
            }
        )

    return theme


def get_icon_theme(variant, mode="light"):
    if mode == "dark":
        default_parent_bg = ("dark", "Basic")
        normal_icon_color = ("neutral", 200)
        hover_bg = ("dark", 600)
    else:
        default_parent_bg = ("neutral", 0)
        normal_icon_color = ("neutral", 400)
        hover_bg = (variant, 150) if variant != "neutral" else ("neutral", 100)

    theme = {
        "normal": normal_icon_color,
        "hover_icon": (variant, "Basic"),
        "hover_bg": hover_bg,
        "active": (variant, 900),
        "parent_bg": default_parent_bg,
    }

    if variant == "neutral" and mode == "light":
        theme["hover_icon"] = ("primary", "Basic")
        theme["hover_bg"] = ("secondary", "Basic")

    return theme
