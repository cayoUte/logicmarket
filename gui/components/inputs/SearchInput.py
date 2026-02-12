import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import gui.utils as utils
from gui.theme.fonts import get_font


def SearchInput(
    parent,
    placeholder="Buscar...",
    width=400,
    height=48,
    radius=24,
    bg_color="#EEF2F6",
    text_color="#1C1B1F",
):
    try:
        parent_bg = parent.cget("bg")
    except:
        parent_bg = "#FFFFFF"

    state = {"image_cache": {}, "current_bg": bg_color}
    canvas = tk.Canvas(
        parent, width=width, height=height, bg=parent_bg, highlightthickness=0, bd=0
    )

    def draw():
        canvas.delete("bg_shape")
        cache_key = (width, height, radius, state["current_bg"], parent_bg)

        if cache_key not in state["image_cache"]:
            scale = 4
            W, H, R = width * scale, height * scale, radius * scale
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw_ctx = ImageDraw.Draw(img)
            draw_ctx.rounded_rectangle(
                (0, 0, W - 1, H - 1), radius=R, fill=state["current_bg"]
            )

            final_img = img.resize((width, height), Image.Resampling.LANCZOS)
            bg_layer = Image.new("RGBA", (width, height), parent_bg)
            bg_layer.paste(final_img, (0, 0), final_img)
            state["image_cache"][cache_key] = ImageTk.PhotoImage(bg_layer)

        tk_bg = state["image_cache"][cache_key]
        canvas.create_image(width / 2, height / 2, image=tk_bg, tags="bg_shape")
        canvas.image_ref = tk_bg
        canvas.tag_lower("bg_shape")

        tk_icon = utils.load_svg_icon(
            "gui/assets/icons/search.svg", 20, "#444746", state["current_bg"]
        )
        canvas.create_image(24, height / 2, image=tk_icon, anchor="center")
        canvas.icon_ref = tk_icon

    draw()
    entry = tk.Entry(
        canvas,
        bg=bg_color,
        bd=0,
        fg=text_color,
        font=get_font("body"),
        highlightthickness=0,
        insertbackground=text_color,
    )
    canvas.create_window(
        48, height / 2, window=entry, width=width - 70, height=height - 14, anchor="w"
    )

    entry.insert(0, placeholder)
    entry.bind(
        "<FocusIn>",
        lambda e: entry.delete(0, "end") if entry.get() == placeholder else None,
    )
    canvas.bind("<Button-1>", lambda e: entry.focus_set())

    return canvas, entry
