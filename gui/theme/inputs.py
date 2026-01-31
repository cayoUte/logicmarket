from gui.theme.app_pallete import APP_PALETTE
INPUT_THEMES = {}
for category in APP_PALETTE.keys():
    INPUT_THEMES[category] = {
        "bg_idle": ("neutral", 25),        
        "bg_focus": ("neutral", 0),        
        "border_idle": ("neutral", 200),   
        "border_focus": (category, "Basic"), 
        "text_color": ("neutral", 900),    
        "placeholder": ("neutral", 400),   
        "height": 35                       
    }