import tkinter as tk
from gui.components.inputs.SearchInput import SearchInput
from gui.theme.fonts import get_font
from gui.utils import get_circle_avatar
from store.selectors import select_current_colors
from store.slices.theme_slice import theme_actions
from store.slices.inventory_slice import actions as inventory_actions


def AppBar(parent, store_funcs, user_data):
    dispatch = store_funcs["dispatch"]
    get_state = store_funcs["get_state"]

    internal_state = {"current_page": "dashboard", "current_title": "Inicio"}

    app_bar = tk.Frame(parent, height=64)
    app_bar.pack_propagate(False)

    app_bar.columnconfigure(0, weight=0)
    app_bar.columnconfigure(1, weight=1)
    app_bar.columnconfigure(2, weight=0)

    left_frame = tk.Frame(app_bar)
    left_frame.grid(row=0, column=0, sticky="w", padx=(24, 12))

    lbl_logo = tk.Label(
        left_frame, text="LOGICMARKET", font=get_font("h5"), cursor="hand2"
    )
    lbl_logo.pack(side="left")

    center_frame = tk.Frame(app_bar)
    center_frame.grid(row=0, column=1, sticky="ew")

    right_frame = tk.Frame(app_bar)
    right_frame.grid(row=0, column=2, sticky="e", padx=(12, 24))

    def toggle_theme():
        dispatch(theme_actions["toggleMode"]())

    btn_theme = tk.Label(
        right_frame, text="🌗", font=("Segoe UI Emoji", 14), cursor="hand2"
    )
    btn_theme.pack(side="left", padx=8)
    btn_theme.bind("<Button-1>", lambda _: toggle_theme())

    btn_notif = tk.Label(
        right_frame, text="🔔", font=("Segoe UI Emoji", 14), cursor="hand2"
    )
    btn_notif.pack(side="left", padx=8)

    sep = tk.Frame(right_frame, width=1, height=24)
    sep.pack(side="left", padx=12)

    avatar_container = tk.Frame(right_frame)
    avatar_container.pack(side="left")

    def render_center_content(colors):
        surface = colors["surface"]
        text = colors["text"]
        input_bg = colors["input_bg"]

        for w in center_frame.winfo_children():
            w.destroy()

        page_id = internal_state["current_page"]

        if page_id in ["importer", "inventory"]:

            search_canvas, search_entry = SearchInput(
                center_frame,
                placeholder="Buscar productos...",
                width=480,
                height=44,
                radius=22,
                bg_color=input_bg,
                text_color=text,
            )
            search_canvas.pack(anchor="center")

            def on_search_change(_):
                query = search_entry.get()
                dispatch(inventory_actions["setSearchParams"]({"query": query}))

            search_entry.bind("<KeyRelease>", on_search_change)

            current_params = get_state()["inventory"].get("search_params", {})
            if current_params.get("query"):
                search_entry.delete(0, tk.END)
                search_entry.insert(0, current_params["query"])
                search_entry.config(fg=text)

        else:
            tk.Label(
                center_frame,
                text=internal_state["current_title"],
                bg=surface,
                fg=text,
                font=get_font("h5"),
            ).pack(anchor="center")

    def update_avatar(surface_color, text_color):
        for w in avatar_container.winfo_children():
            w.destroy()
        try:
            img = get_circle_avatar(
                user_data.get("avatar_path"), size=(32, 32), bg_color=surface_color
            )
            if img:
                l = tk.Label(
                    avatar_container, image=img, bg=surface_color, cursor="hand2"
                )
                l.image = img
                l.pack()
                return
        except:
            pass

        tk.Label(
            avatar_container,
            text="👤",
            bg=surface_color,
            fg=text_color,
            font=("Arial", 16),
        ).pack()

    def update_theme_visuals():
        colors = select_current_colors(get_state())

        surface = colors["surface"]
        text = colors["text"]

        app_bar.config(bg=surface)
        left_frame.config(bg=surface)
        center_frame.config(bg=surface)
        right_frame.config(bg=surface)
        avatar_container.config(bg=surface)

        lbl_logo.config(bg=surface, fg=text)
        btn_theme.config(bg=surface, fg=text)
        btn_notif.config(bg=surface, fg=text)

        sep_color = "#E0E2E5" if text == "#1A1C1E" else "#49454F"
        sep.config(bg=sep_color)

        update_avatar(surface, text)
        render_center_content(colors)

    def update_route(page_id, title=""):
        internal_state["current_page"] = page_id
        internal_state["current_title"] = title
        update_theme_visuals()

    update_theme_visuals()

    return {
        "widget": app_bar,
        "update_route": update_route,
        "update_theme": update_theme_visuals,
    }
