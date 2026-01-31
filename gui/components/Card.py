import tkinter as tk
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from gui.components.buttons.IconButton import IconButton
from gui.theme.app_pallete import get_app_color
from gui.theme.cards import CARD_THEMES
from gui.theme.fonts import get_font

def Card(parent, title, body_text="", variant="elevated", parent_bg=None, dimensions=(280, 160), on_menu_click=None):
    """
    Material 3 Style Card Component.
    
    Args:
        dimensions: (width, height)
        variant: "elevated", "filled", or "outlined"
    """
    width, height = dimensions
    corner_radius = 12 # 12dp corner radius from image_b83d20.png
    padding = 16       # 16dp left/right padding from image_b83d20.png
    
    theme = CARD_THEMES.get(variant, CARD_THEMES["elevated"])

    def resolve(val):
        if val is None: return None
        return get_app_color(val[0], val[1])

    state = {
        "bg": resolve(theme["bg"]),
        "border": resolve(theme["border"]),
        "title_color": resolve(theme["text_title"]),
        "body_color": resolve(theme["text_body"]),
        "parent_bg": parent_bg if parent_bg else get_app_color("neutral", 0) # Base para blending
    }

    # --- CANVAS ---
    canvas = tk.Canvas(
        parent, width=width, height=height, 
        bg=state["parent_bg"], highlightthickness=0
    )

    # --- PIL IMAGE GENERATOR (Rounded + Shadow) ---
    def generate_card_bg():
        scale = 4
        W, H, R = width * scale, height * scale, corner_radius * scale
        
        # Create image with alpha
        img = Image.new('RGBA', (W, H), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        # Shadow simulation for elevated cards
        if theme["shadow"]:
            # Basic shadow layer
            shadow_offset = 2 * scale
            draw.rounded_rectangle(
                (shadow_offset, shadow_offset, W-1, H-1), 
                R, fill=(0,0,0,30) # Soft shadow
            )
            img = img.filter(ImageFilter.GaussianBlur(radius=scale))
            draw = ImageDraw.Draw(img)

        # Main Shape
        outline_col = state["border"] if state["border"] else None
        draw.rounded_rectangle(
            (0, 0, W-(4*scale if theme["shadow"] else 1), H-(4*scale if theme["shadow"] else 1)), 
            R, fill=state["bg"], outline=outline_col, width=1*scale if outline_col else 0
        )
        
        return ImageTk.PhotoImage(img.resize((width, height), Image.LANCZOS))

    # Render BG
    tk_bg = generate_card_bg()
    canvas.create_image(width/2, height/2, image=tk_bg)
    canvas.bg_ref = tk_bg

    # --- CONTENT (Start-aligned as per measurements) ---
    # Title
    canvas.create_text(
        padding, padding, 
        text=title, 
        font=get_font("h3"), # Montserrat Bold
        fill=state["title_color"], 
        anchor="nw"
    )

    # Body Text
    if body_text:
        canvas.create_text(
            padding, padding + 30, 
            text=body_text, 
            font=get_font("body"), # Segoe UI
            fill=state["body_color"], 
            anchor="nw",
            width=width - (padding * 2)
        )

    # Menu Icon (The three dots from image_b83d5c.png)
    if on_menu_click:
        menu_btn = IconButton(
            canvas, 
            icon_path="more_vert.svg", 
            on_click=on_menu_click, 
            size=18, 
            bg_parent= state["bg"],
            variant="neutral"
        )
        canvas.create_window(width - padding, padding, window=menu_btn, anchor="ne")

    return canvas