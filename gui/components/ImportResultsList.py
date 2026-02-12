import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import requests
from io import BytesIO
import threading
import os
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font

IMAGE_CACHE = {}
APP_LOGO_CACHE = None


def ImportResultsList(parent, on_import_click=None, height=400, colors=None):

    if not colors:
        colors = {"background": "#ffffff", "surface": "#ffffff", "text": "#000000"}

    BG_COLOR = colors.get("background", "#ffffff")
    TEXT_PRIMARY = colors.get("text", "#000000")

    is_dark = (
        BG_COLOR.startswith("#1") or BG_COLOR.startswith("#2") or BG_COLOR == "#000000"
    )

    if is_dark:
        HOVER_COLOR = get_app_color("dark", 600)
        DIVIDER_COLOR = get_app_color("dark", 500)
        TEXT_SECONDARY = "#CAC4D0"
        AVATAR_BG = get_app_color("primary", 800)
        BTN_TEXT_COLOR = get_app_color("primary", 200)
    else:
        HOVER_COLOR = get_app_color("neutral", 50)
        DIVIDER_COLOR = get_app_color("neutral", 100)
        TEXT_SECONDARY = get_app_color("neutral", 400)
        AVATAR_BG = get_app_color("primary", 50)
        BTN_TEXT_COLOR = get_app_color("primary", "Basic")

    container = tk.Frame(parent, bg=BG_COLOR, height=height)
    container.pack_propagate(False)

    canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0, bd=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def make_circle(pil_img, size):
        pil_img = pil_img.resize((size, size), Image.LANCZOS).convert("RGBA")
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        output.paste(pil_img, (0, 0), mask=mask)
        return output

    def create_placeholder_initials(text, size=40):
        scale = 4
        W, H = size * scale, size * scale
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, W, H), fill=AVATAR_BG)
        return ImageTk.PhotoImage(img.resize((size, size), Image.LANCZOS))

    def get_app_logo_image(size=40):
        global APP_LOGO_CACHE
        if APP_LOGO_CACHE:
            return APP_LOGO_CACHE
        logo_path = "gui/assets/images/logicmarket_logo.png"
        try:
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                APP_LOGO_CACHE = ImageTk.PhotoImage(make_circle(img, size))
            else:
                APP_LOGO_CACHE = create_placeholder_initials("?", size)
        except Exception:
            APP_LOGO_CACHE = create_placeholder_initials("?", size)
        return APP_LOGO_CACHE

    def load_remote_image(url, target_widget, size=40):
        if not url:
            return
        if url in IMAGE_CACHE:
            _update_label_image(target_widget, IMAGE_CACHE[url])
            return

        def thread_task():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    img_data = response.content
                    pil_img = Image.open(BytesIO(img_data))
                    photo = ImageTk.PhotoImage(make_circle(pil_img, size))
                    IMAGE_CACHE[url] = photo
                    target_widget.after(
                        0, lambda: _update_label_image(target_widget, photo)
                    )
            except Exception:
                logo_img = get_app_logo_image(size)
                target_widget.after(
                    0, lambda: _update_label_image(target_widget, logo_img)
                )

        threading.Thread(target=thread_task, daemon=True).start()

    def _update_label_image(widget, photo):
        if widget.winfo_exists():
            widget.configure(image=photo)
            widget.image = photo

    def create_row(product, is_last=False):
        row = tk.Frame(scrollable_frame, bg=BG_COLOR, pady=12, padx=16)
        row.pack(fill="x", anchor="n")

        image_url = product.get("image_url")
        lbl_avatar = tk.Label(row, bg=BG_COLOR)

        if image_url:
            initial = (product.get("brand") or product.get("name") or "?")[0].upper()
            _update_label_image(
                lbl_avatar, create_placeholder_initials(initial, size=40)
            )
            load_remote_image(image_url, lbl_avatar, size=40)
        else:
            _update_label_image(lbl_avatar, get_app_logo_image(size=40))

        lbl_avatar.pack(side="left", padx=(0, 16))

        text_container = tk.Frame(row, bg=BG_COLOR)
        text_container.pack(side="left", fill="x", expand=True)

        product_name = product.get("name", "Desconocido")
        tk.Label(
            text_container,
            text=product_name[:50] + ("..." if len(product_name) > 50 else ""),
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            font=get_font("h5"),
            anchor="w",
        ).pack(fill="x")

        meta_text = (
            f"{product.get('brand', 'Sin Marca')} • {product.get('code', 'S/N')}"
        )
        tk.Label(
            text_container,
            text=meta_text,
            bg=BG_COLOR,
            fg=TEXT_SECONDARY,
            font=get_font("caption"),
            anchor="w",
        ).pack(fill="x")

        btn_import = tk.Button(
            row,
            text="IMPORTAR",
            bg=BG_COLOR,
            fg=BTN_TEXT_COLOR,
            font=("Arial", 9, "bold"),
            relief="flat",
            activebackground=HOVER_COLOR,
            activeforeground=BTN_TEXT_COLOR,
            cursor="hand2",
            bd=0,
            command=lambda p=product: on_import_click(p) if on_import_click else None,
        )
        btn_import.pack(side="right", padx=(16, 0))

        if not is_last:
            tk.Frame(scrollable_frame, bg=DIVIDER_COLOR, height=1).pack(
                fill="x", padx=(72, 0)
            )

        def on_enter(e):
            row.configure(bg=HOVER_COLOR)
            text_container.configure(bg=HOVER_COLOR)
            lbl_avatar.configure(bg=HOVER_COLOR)
            btn_import.configure(bg=HOVER_COLOR)

        def on_leave(e):
            row.configure(bg=BG_COLOR)
            text_container.configure(bg=BG_COLOR)
            lbl_avatar.configure(bg=BG_COLOR)
            btn_import.configure(bg=BG_COLOR)

        for widget in [row, text_container, lbl_avatar]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def set_data(products):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not products:
            tk.Label(
                scrollable_frame, text="Sin resultados", bg=BG_COLOR, fg=TEXT_SECONDARY
            ).pack(pady=20)
            return

        for i, p in enumerate(products):
            create_row(p, is_last=(i == len(products) - 1))

    container.set_data = set_data
    return container
