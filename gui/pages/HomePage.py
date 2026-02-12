import os
import tkinter as tk
from PIL import Image, ImageTk
from gui.components.buttons.Button import Pillow_Button
from gui.theme.app_pallete import get_app_color
from gui.theme.fonts import get_font


def HomePage(parent, on_navigate):

    bg_color = get_app_color("neutral", 0)
    primary_col = get_app_color("primary", "Basic")
    text_sec_col = get_app_color("neutral", 600)

    root_frame = tk.Frame(parent, bg=bg_color)

    canvas = tk.Canvas(root_frame, bg=bg_color, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    scroll_frame = tk.Frame(canvas, bg=bg_color)
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def create_hero_section(container):
        frame = tk.Frame(container, bg=bg_color)

        center = tk.Frame(frame, bg=bg_color)
        center.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

        try:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_name = "logicmarket_logo.png"
            original_img = Image.open(os.path.join(base_path, "assets", file_name))
            base_height = 100
            ratio = base_height / float(original_img.size[1])
            w_size = int(float(original_img.size[0]) * float(ratio))
            img = ImageTk.PhotoImage(
                original_img.resize((w_size, base_height), Image.LANCZOS)
            )

            lbl = tk.Label(center, image=img, bg=bg_color)
            lbl.image = img
            lbl.pack(pady=(0, 20))
        except:
            tk.Label(
                center,
                text="LogicMarket",
                font=get_font("h1"),
                fg=primary_col,
                bg=bg_color,
            ).pack(pady=(0, 20))

        tk.Label(
            center,
            text="Control Total de tu Inventario.",
            font=get_font("h1"),
            fg=primary_col,
            bg=bg_color,
        ).pack()
        tk.Label(
            center,
            text="Sin Complicaciones.",
            font=get_font("h1"),
            fg=primary_col,
            bg=bg_color,
        ).pack(pady=(0, 10))

        tk.Label(
            center,
            text="Centraliza productos, visualiza stock y elimina errores manuales con nuestro sistema lógico.",
            font=get_font("h3"),
            fg=text_sec_col,
            bg=bg_color,
            wraplength=700,
        ).pack(pady=(0, 40))

        btn = Pillow_Button(
            center,
            text="Ver Beneficios ↓",
            on_click=lambda: scroll_to_page(1),
            dimensions=(200, 50, 25),
            variant="secondary",
        )
        btn.pack()

        return frame

    def create_benefits_section(container):
        frame = tk.Frame(container, bg=bg_color)

        center = tk.Frame(frame, bg=bg_color)
        center.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

        tk.Label(
            center,
            text="¿Por qué elegirnos?",
            font=get_font("h2"),
            fg=primary_col,
            bg=bg_color,
        ).pack(pady=(0, 40))

        grid = tk.Frame(center, bg=bg_color)
        grid.pack(fill="x")

        def add_card(parent, icon_char, title, desc):
            card = tk.Frame(parent, bg=get_app_color("neutral", 25), padx=20, pady=20)
            tk.Label(
                card,
                text=icon_char,
                font=("Segoe UI Emoji", 30),
                bg=get_app_color("neutral", 25),
            ).pack()
            tk.Label(
                card,
                text=title,
                font=get_font("h3"),
                fg=primary_col,
                bg=get_app_color("neutral", 25),
            ).pack(pady=10)
            tk.Label(
                card,
                text=desc,
                font=get_font("body"),
                fg=text_sec_col,
                bg=get_app_color("neutral", 25),
                wraplength=200,
            ).pack()
            return card

        c1 = add_card(
            grid, "⚡", "Eficiencia", "Reduce tiempo administrativo en un 40%."
        )
        c1.pack(side="left", expand=True, fill="both", padx=10)

        c2 = add_card(grid, "🎯", "Precisión", "Alertas de stock bajo automáticas.")
        c2.pack(side="left", expand=True, fill="both", padx=10)

        c3 = add_card(grid, "📈", "Escalabilidad", "Crece sin cambiar de software.")
        c3.pack(side="left", expand=True, fill="both", padx=10)

        Pillow_Button(
            center,
            text="Comenzar Ahora",
            on_click=lambda: on_navigate("dashboard"),
            dimensions=(220, 55, 27),
            variant="primary",
        ).pack(pady=(50, 0))

        return frame

    section1 = create_hero_section(scroll_frame)
    section2 = create_benefits_section(scroll_frame)

    sections = [section1, section2]
    current_page = [0]

    def update_layout(event=None):
        win_width = root_frame.winfo_width()
        win_height = root_frame.winfo_height()

        if win_height < 100:
            return

        total_h = win_height * len(sections)
        canvas.itemconfig(canvas_window, width=win_width, height=total_h)
        canvas.configure(scrollregion=(0, 0, win_width, total_h))

        for sec in sections:
            sec.place(x=0, width=win_width, height=win_height)

        section1.place(y=0)
        section2.place(y=win_height)

        scroll_to_page(current_page[0], animate=False)

    def scroll_to_page(page_index, animate=True):
        if page_index < 0 or page_index >= len(sections):
            return

        current_page[0] = page_index

        total_pages = len(sections)
        target_pos = page_index / total_pages

        if animate:
            smooth_scroll(target_pos)
        else:
            canvas.yview_moveto(target_pos)

    def smooth_scroll(target_pos):
        current_pos = canvas.yview()[0]
        diff = target_pos - current_pos

        if abs(diff) < 0.001:
            canvas.yview_moveto(target_pos)
            return

        step = diff * 0.2
        canvas.yview_moveto(current_pos + step)
        root_frame.after(10, lambda: smooth_scroll(target_pos))

    scroll_state = {"scrolling": False}

    def on_mouse_wheel(event):
        if scroll_state["scrolling"]:
            return

        delta = 0
        if event.num == 5 or event.delta < 0:
            delta = 1
        elif event.num == 4 or event.delta > 0:
            delta = -1

        if delta != 0:
            next_idx = current_page[0] + delta
            if 0 <= next_idx < len(sections):
                scroll_state["scrolling"] = True
                scroll_to_page(next_idx)
                root_frame.after(600, lambda: scroll_state.update({"scrolling": False}))

    root_frame.bind("<Configure>", update_layout)

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Button-4>", on_mouse_wheel)
    canvas.bind_all("<Button-5>", on_mouse_wheel)

    def on_destroy(e):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    root_frame.bind("<Destroy>", on_destroy)

    return root_frame
