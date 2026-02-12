def get_dialog_theme(mode="light"):
    if mode == "dark":
        return {
            "bg": ("dark", 750),
            "title": ("neutral", 50),
            "body": ("neutral", 200),
            "card_bg": ("dark", 700),
            "overlay": "#000000",
        }
    else:
        return {
            "bg": ("neutral", 0),
            "title": ("neutral", 900),
            "body": ("neutral", 700),
            "card_bg": ("neutral", 25),
            "overlay": "#000000",
        }


DIALOG_SPECS = {
    "padding_outer": 24,
    "padding_title": 16,
    "padding_actions": 24,
    "gap_actions": 8,
    "radius": 28,
    "min_width": 320,
    "max_width": 560,
}
