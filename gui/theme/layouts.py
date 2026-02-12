from gui.theme.app_pallete import get_app_color


def get_drawer_theme(mode="light"):
    if mode == "dark":
        return {
            "bg": ("dark", "Basic"),
            "border": ("dark", 600),
            "icon_variant": "secondary",
        }
    else:
        return {
            "bg": ("neutral", 0),
            "border": ("neutral", 200),
            "icon_variant": "secondary",
        }
