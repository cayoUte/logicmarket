import tkinter as tk
from gui.theme.app_pallete import get_app_color
from gui.components.buttons.IconButton import IconButton
from gui.theme.layouts import get_drawer_theme


def PersistentDrawer(
    parent, nav_items, on_navigate, width=70, ui_mode="light", variant="primary"
):
    """
    Barra lateral funcional y reactiva al tema.
    """

    theme = get_drawer_theme(mode=ui_mode)

    def resolve(val):
        return get_app_color(val[0], val[1]) if isinstance(val, (tuple, list)) else val

    bg_color = resolve(theme["bg"])
    border_color = resolve(theme["border"])

    icon_variant = variant if variant != "primary" else theme["icon_variant"]

    frame = tk.Frame(parent, width=width, bg=bg_color)
    frame.pack_propagate(False)

    buttons_registry = {}
    state = {"current_id": None}

    def handle_selection(target_id):
        if state["current_id"] == target_id:
            return

        old_id = state["current_id"]
        if old_id and old_id in buttons_registry:
            if hasattr(buttons_registry[old_id], "set_selected"):
                buttons_registry[old_id].set_selected(False)

        if target_id in buttons_registry:
            if hasattr(buttons_registry[target_id], "set_selected"):
                buttons_registry[target_id].set_selected(True)
            state["current_id"] = target_id

        if on_navigate:
            on_navigate(target_id)

    tk.Frame(frame, height=20, bg=bg_color).pack()

    for item in nav_items:
        item_id = item["id"]
        icon_path = item["icon"]

        def on_btn_click(uid=item_id):
            handle_selection(uid)

        btn_widget = IconButton(
            frame,
            icon_path=icon_path,
            on_click=on_btn_click,
            size=24,
            variant=icon_variant,
            bg_parent=bg_color,
            ui_mode=ui_mode,
        )
        btn_widget.pack(pady=8)

        buttons_registry[item_id] = btn_widget

    border = tk.Frame(frame, bg=border_color, width=1)
    border.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

    frame.select_item = handle_selection

    return frame
