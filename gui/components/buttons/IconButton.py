from gui.theme.app_pallete import get_app_color
from gui.theme.buttons import ICON_THEMES
import tkinter as tk
import gui.utils as utils


def IconButton(
    parent, icon_path, on_click, size=24, bg_parent=None, variant="primary", is_selected=False
):
    """
    Args:
        is_selected (bool): If True, the button renders in its 'Active/Hover' state permanently.
    """

    theme = ICON_THEMES.get(variant, ICON_THEMES["primary"])

    def resolve_color(value):
        if isinstance(value, (tuple, list)) and len(value) == 2:
            return get_app_color(value[0], value[1])
        return value

    state = {
        "hover": False,
        "pressed": False,
        "selected": is_selected,
        "bg_parent": resolve_color(theme["parent_bg"]),
        "color_normal": resolve_color(theme["normal"]),
        "color_hover": resolve_color(theme["hover_icon"]),
        "bg_hover": resolve_color(theme["hover_bg"]),
        "color_active": resolve_color(theme["active"]),
        "image_cache": {},
    }

    padding = 8
    canvas_size = size + (padding * 2)

    canvas = tk.Canvas(
        parent,
        width=canvas_size,
        height=canvas_size,
        bg= bg_parent if bg_parent else state["bg_parent"],
        highlightthickness=0,
        cursor="hand2",
    )

    def draw(offset=0):
        canvas.delete("all")

        is_active = state["hover"] or state["selected"]

        if state["pressed"]:
            icon_color = state["color_active"]
            bg_circle_color = state["bg_hover"]
            offset = 1
        elif is_active:
            icon_color = state["color_hover"]
            bg_circle_color = state["bg_hover"]
        else:
            icon_color = state["color_normal"]
            bg_circle_color = bg_parent if bg_parent else state["bg_parent"]

        center = int(canvas_size / 2) + offset

        if is_active or state["pressed"]:
            circle_key = f"circle_{bg_circle_color}_{canvas_size}"
            if circle_key not in state["image_cache"]:
                state["image_cache"][circle_key] = utils.get_circle_image(
                    canvas_size - 2, bg_circle_color, state["bg_parent"]
                )
            canvas.create_image(
                center, center, image=state["image_cache"][circle_key], anchor="center"
            )

        icon_key = f"icon_{icon_path}_{icon_color}_{state['bg_parent']}"
        if icon_key not in state["image_cache"]:
            full_path = f"gui/assets/icons/{icon_path}"

            bg_camu = (
                bg_circle_color
                if (is_active or state["pressed"])
                else state["bg_parent"]
            )
            state["image_cache"][icon_key] = utils.load_svg_icon(
                full_path, size, icon_color, bg_camu
            )

        tk_icon = state["image_cache"][icon_key]
        if tk_icon:
            canvas.create_image(center, center, image=tk_icon, anchor="center")
            canvas.icon_image = tk_icon

    draw()

    def set_selection_state(is_active):
        state["selected"] = is_active
        draw()

    canvas.set_selected = set_selection_state

    def on_enter(e):
        state["hover"] = True
        draw()

    def on_leave(e):
        state["hover"] = False
        state["pressed"] = False
        draw()

    def on_press(e):
        state["pressed"] = True
        draw()

    def on_release(e):
        if state["pressed"]:
            state["pressed"] = False
            draw()
            if 0 <= e.x <= canvas_size and 0 <= e.y <= canvas_size and on_click:
                on_click()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)

    return canvas
