from gui.theme.app_pallete import APP_PALETTE


def get_input_theme(variant, mode="light"):
    if mode == "dark":
        bg_idle = ("dark", 800)
        bg_focus = ("dark", 800)
        border_idle = ("dark", 500)
        text_color = ("neutral", 50)
        placeholder = ("neutral", 400)
        cursor = ("neutral", 0)
    else:
        bg_idle = ("neutral", 0)
        bg_focus = ("neutral", 0)
        border_idle = ("neutral", 200)
        text_color = ("neutral", 900)
        placeholder = ("neutral", 400)
        cursor = ("neutral", 900)

    if variant in APP_PALETTE:
        border_focus = (variant, "Basic")
    else:
        border_focus = ("primary", "Basic")

    return {
        "bg_idle": bg_idle,
        "bg_focus": bg_focus,
        "border_idle": border_idle,
        "border_focus": border_focus,
        "text_color": text_color,
        "placeholder": placeholder,
        "cursor": cursor,
        "height": 40,
        "radius": 8,
    }


def get_textfield_theme(mode="light"):
    if mode == "dark":
        return {
            "bg_idle": ("dark", 700),
            "bg_hover": ("dark", 600),
            "indicator_idle": ("neutral", 500),
            "indicator_focus": ("primary", "Basic"),
            "indicator_error": ("error", "Basic"),
            "label_idle": ("neutral", 300),
            "label_focus": ("primary", "Basic"),
            "label_error": ("error", "Basic"),
            "text": ("neutral", 50),
            "caret": ("primary", "Basic"),
            "supporting": ("neutral", 400),
            "supporting_error": ("error", "Basic"),
        }
    else:
        return {
            "bg_idle": ("neutral", 25),
            "bg_hover": ("neutral", 50),
            "indicator_idle": ("neutral", 400),
            "indicator_focus": ("primary", "Basic"),
            "indicator_error": ("error", "Basic"),
            "label_idle": ("neutral", 400),
            "label_focus": ("primary", "Basic"),
            "label_error": ("error", "Basic"),
            "text": ("neutral", 900),
            "caret": ("primary", "Basic"),
            "supporting": ("neutral", 400),
            "supporting_error": ("error", "Basic"),
        }
