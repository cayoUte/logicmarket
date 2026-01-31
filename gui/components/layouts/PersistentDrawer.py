import tkinter as tk
from gui.theme.app_pallete import get_app_color
from gui.components.buttons.IconButton import IconButton


def PersistentDrawer(parent, nav_items, on_navigate, width=70, variant="primary"):
    """
    Functional Sidebar Component.

    Args:
        nav_items: List of dicts [{'icon': 'home.svg', 'id': 'home'}, ...]
        on_navigate: Callback function(item_id)
        variant: Palette key for the active selection color.
    """

    bg_color = get_app_color("neutral", 0)
    border_color = get_app_color("neutral", 200)

    frame = tk.Frame(parent, width=width, bg=bg_color)
    frame.pack_propagate(False)

    buttons_registry = {}
    state = {"current_id": None}

    def handle_selection(target_id):

        if state["current_id"] == target_id:
            return

        old_id = state["current_id"]
        if old_id and old_id in buttons_registry:

            buttons_registry[old_id].set_selected(False)

        if target_id in buttons_registry:
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
            frame, icon_path=icon_path, on_click=on_btn_click, size=24, variant=variant
        )
        btn_widget.pack(pady=8)

        buttons_registry[item_id] = btn_widget

    border = tk.Frame(frame, bg=border_color, width=1)
    border.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

    frame.select_item = handle_selection

    return frame
