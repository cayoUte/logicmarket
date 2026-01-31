from gui.theme.app_pallete import APP_PALETTE

BUTTON_THEMES = {}
for category in APP_PALETTE.keys():
    BUTTON_THEMES[category] = {
        "main": (category, "Basic"),
        "hover": (category, 600),
        "active": (category, 800),
        "text": ("neutral", 0),
        "parent_bg": ("neutral", 0),
        "border": None 
    }
BUTTON_THEMES["surface"] = {
    "main": ("neutral", 0),       
    "hover": ("neutral", 50),     
    "active": ("neutral", 100),   
    "text": ("neutral", 900),     
    "parent_bg": ("neutral", 0),
    "border": ("neutral", 200)    
}
BUTTON_THEMES["dark"] = {
    "main": ("primary", 900),     
    "hover": ("primary", 800),
    "active": ("primary", 1000),
    "text": ("neutral", 0),
    "parent_bg": ("neutral", 0),
    "border": None
}
ICON_THEMES = {}
for category in APP_PALETTE.keys():
    ICON_THEMES[category] = {
        "normal": ("neutral", 400),
        "hover_icon": (category, "Basic"),
        "hover_bg": (category, 50),
        "active": (category, 800),
        "parent_bg": ("neutral", 0),
    }

ICON_THEMES["neutral"]["hover_icon"] = ("neutral", 900)
ICON_THEMES["neutral"]["hover_bg"] = ("neutral", 100)
